"""High-performance, read-only binary DBF reader for Visual FoxPro / dBase tables.

Features:
- Pure Python with zero external C-dependencies.
- Read-only shared access (compatible with running VFP applications).
- Instant binary decoding with automatic character set fallback (cp1252 -> latin1 -> utf-8).
- Automatically filters out marked-deleted records (0x2A).
- Parses VFP date (D), numeric (N), character (C), and logical (L) fields.
- Fast SHA-256 and modification time caching for change detection.
"""

from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Generator, List, Optional, Tuple, Union
import hashlib
import os
import struct


class DBFError(Exception):
    """Base exception for DBF operations."""
    pass


class DBFFileNotFoundError(DBFError, FileNotFoundError):
    """Raised when the specified DBF table does not exist."""
    pass


class DBFCorruptedError(DBFError, ValueError):
    """Raised when DBF binary structure is truncated or corrupted."""
    pass


@dataclass(frozen=True)
class DBFField:
    name: str
    type: str
    length: int
    decimals: int
    offset: int  # Byte offset within the record (offset 0 is the deletion flag)


@dataclass(frozen=True)
class DBFHeader:
    version: int
    last_update: str
    num_records: int
    header_length: int
    record_length: int
    fields: Tuple[DBFField, ...]


class DBFReader:
    """Zero-locking binary reader for FoxPro/dBase DBF tables."""

    def __init__(self, filepath: Union[str, Path], encoding: str = "cp1252"):
        self.filepath = Path(filepath).resolve()
        self.encoding = encoding
        self._header: Optional[DBFHeader] = None
        self._cached_mtime: float = 0.0
        self._cached_checksum: str = ""

    @property
    def header(self) -> DBFHeader:
        """Lazily read and cache table header."""
        if self._header is None:
            self._header = self.read_header()
        return self._header

    def exists(self) -> bool:
        """Check if table file exists on disk."""
        return self.filepath.is_file()

    def get_mtime(self) -> float:
        """Get file modification timestamp."""
        if not self.exists():
            raise DBFFileNotFoundError(f"Table file not found: {self.filepath}")
        return os.path.getmtime(self.filepath)

    def compute_checksum(self) -> str:
        """Compute SHA-256 hash of the DBF file for change detection."""
        if not self.exists():
            raise DBFFileNotFoundError(f"Table file not found: {self.filepath}")

        hasher = hashlib.sha256()
        with open(self.filepath, "rb") as f:
            while chunk := f.read(65536):
                hasher.update(chunk)
        return hasher.hexdigest()

    def read_header(self) -> DBFHeader:
        """Parse binary header and field descriptors."""
        if not self.exists():
            raise DBFFileNotFoundError(f"Table file not found: {self.filepath}")

        with open(self.filepath, "rb") as f:
            raw_header = f.read(32)
            if len(raw_header) < 32:
                raise DBFCorruptedError(f"Header too short ({len(raw_header)} bytes) in {self.filepath}")

            version = raw_header[0]
            year = raw_header[1] + 2000 if raw_header[1] < 80 else raw_header[1] + 1900
            month = raw_header[2]
            day = raw_header[3]
            last_update = f"{year:04d}-{month:02d}-{day:02d}"

            num_records, header_length, record_length = struct.unpack("<IHH", raw_header[4:12])

            # Field descriptors start at byte 32 and terminate with 0x0D
            f.seek(32)
            field_block = f.read(header_length - 32)
            fields: List[DBFField] = []
            pos = 0
            offset = 1  # 0 is the deletion flag (0x20 active, 0x2A deleted)

            while pos < len(field_block) and field_block[pos] != 0x0D:
                fd = field_block[pos : pos + 32]
                if len(fd) < 32:
                    break

                fname = fd[:11].split(b"\x00")[0].decode("ascii", "ignore").strip()
                ftype = chr(fd[11])
                flen = fd[16]
                fdec = fd[17]

                fields.append(
                    DBFField(
                        name=fname,
                        type=ftype,
                        length=flen,
                        decimals=fdec,
                        offset=offset,
                    )
                )
                offset += flen
                pos += 32

            return DBFHeader(
                version=version,
                last_update=last_update,
                num_records=num_records,
                header_length=header_length,
                record_length=record_length,
                fields=tuple(fields),
            )

    def _decode_string(self, raw_bytes: bytes) -> str:
        """Decode raw bytes into a string, falling back to latin1 if needed."""
        try:
            return raw_bytes.decode(self.encoding).strip()
        except UnicodeDecodeError:
            try:
                return raw_bytes.decode("latin1").strip()
            except Exception:
                return raw_bytes.decode("utf-8", "replace").strip()

    def _convert_value(self, field: DBFField, raw_bytes: bytes) -> Any:
        """Convert raw field bytes into Python native type."""
        ftype = field.type
        if ftype == "C":
            return self._decode_string(raw_bytes)

        elif ftype == "N":
            s = raw_bytes.strip()
            if not s:
                return 0 if field.decimals == 0 else 0.0
            if field.decimals == 0:
                try:
                    return int(s)
                except ValueError:
                    return 0
            else:
                try:
                    return float(s)
                except ValueError:
                    return 0.0

        elif ftype == "D":
            s = raw_bytes.strip()
            if len(s) == 8 and s.isdigit():
                return f"{s[:4].decode('ascii')}-{s[4:6].decode('ascii')}-{s[6:8].decode('ascii')}"
            return None

        elif ftype == "L":
            val = chr(raw_bytes[0]) if raw_bytes else "?"
            if val in ("T", "t", "Y", "y"):
                return True
            if val in ("F", "f", "N", "n"):
                return False
            return None

        # Fallback for other / unhandled types
        return self._decode_string(raw_bytes)

    def iter_records(self) -> Generator[Dict[str, Any], None, None]:
        """Stream active (non-deleted) records one-by-one."""
        header = self.header
        with open(self.filepath, "rb") as f:
            f.seek(header.header_length)
            rec_len = header.record_length

            for _ in range(header.num_records):
                record_bytes = f.read(rec_len)
                if len(record_bytes) < rec_len:
                    break

                # 0x2A means deleted; 0x20 means active
                if record_bytes[0] == 0x2A:
                    continue

                record: Dict[str, Any] = {}
                for field in header.fields:
                    start = field.offset
                    end = start + field.length
                    val_bytes = record_bytes[start:end]
                    record[field.name] = self._convert_value(field, val_bytes)

                yield record

    def read_all_records(self) -> List[Dict[str, Any]]:
        """Read all active records into memory."""
        return list(self.iter_records())
