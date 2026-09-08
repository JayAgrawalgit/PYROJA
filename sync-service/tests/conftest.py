"""Pytest fixtures and configuration."""

import shutil
import struct
import tempfile
from pathlib import Path
import pytest

from app.config import AppConfig, FoxproConfig, DatabaseConfig, CacheConfig
from app.services.master_service import MasterDataService
from app.main import create_app
from fastapi.testclient import TestClient


@pytest.fixture
def real_data_config(tmp_path) -> AppConfig:
    """Config pointing to real legacy DBF tables with an isolated temporary SQLite database."""
    base_dir = Path(__file__).resolve().parent.parent
    data_path = (base_dir / "../legacy-software-extracted/FAVWIN/D2627").resolve()
    test_db = tmp_path / "test_isolated_state.sqlite3"
    return AppConfig(
        foxpro=FoxproConfig(
            data_path=data_path,
            active_fiscal_year="D2627",
        ),
        database=DatabaseConfig(
            path=test_db,
        ),
        cache=CacheConfig(
            ttl_seconds=5,
            validate_mtime=True,
        ),
    )


@pytest.fixture
def test_client(real_data_config) -> TestClient:
    """FastAPI TestClient using real FoxPro tables and isolated temporary SQLite DB."""
    app = create_app(real_data_config)
    with TestClient(app) as client:
        yield client


@pytest.fixture
def temp_dbf_dir():
    """Temporary directory for creating synthetic DBF tables."""
    temp_dir = tempfile.mkdtemp(prefix="pyro_test_dbf_")
    yield Path(temp_dir)
    shutil.rmtree(temp_dir, ignore_errors=True)


def create_synthetic_dbf(
    filepath: Path,
    fields: list,  # [(name, type, len, dec)]
    records: list,  # [ {col: val} ]
    deleted_indices: list = None,
):
    """Utility to generate valid dBase III / FoxPro binary DBF files for tests."""
    deleted_indices = deleted_indices or []
    num_recs = len(records)
    header_len = 32 + len(fields) * 32 + 1  # 0x0D terminator
    rec_len = 1 + sum(f[2] for f in fields)  # 1 byte for deletion flag

    # 1. Write Header (32 bytes)
    header = bytearray(32)
    header[0] = 0x30  # VFP version
    header[1] = 26    # Year (2026 - 2000)
    header[2] = 9     # Month
    header[3] = 7     # Day
    struct.pack_into("<I", header, 4, num_recs)
    struct.pack_into("<H", header, 8, header_len)
    struct.pack_into("<H", header, 10, rec_len)

    with open(filepath, "wb") as f:
        f.write(header)

        # 2. Write Field Descriptors (32 bytes each)
        for fname, ftype, flen, fdec in fields:
            fd = bytearray(32)
            name_bytes = fname.encode("ascii")[:10]
            fd[: len(name_bytes)] = name_bytes
            fd[11] = ord(ftype)
            fd[16] = flen
            fd[17] = fdec
            f.write(fd)

        # Terminator
        f.write(b"\x0D")

        # 3. Write Records
        for idx, row in enumerate(records):
            rec = bytearray(rec_len)
            rec[0] = 0x2A if idx in deleted_indices else 0x20  # deletion flag

            offset = 1
            for fname, ftype, flen, fdec in fields:
                val = row.get(fname, "")
                if ftype == "C":
                    val_bytes = str(val).encode("cp1252")[:flen]
                    rec[offset : offset + len(val_bytes)] = val_bytes
                    for k in range(offset + len(val_bytes), offset + flen):
                        rec[k] = 0x20
                elif ftype == "N":
                    if fdec == 0:
                        fmt_str = f"{int(val):>{flen}d}"
                    else:
                        fmt_str = f"{float(val):>{flen}.{fdec}f}"
                    fmt_bytes = fmt_str.encode("ascii")[:flen]
                    rec[offset : offset + len(fmt_bytes)] = fmt_bytes
                offset += flen

            f.write(rec)
