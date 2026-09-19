"""Read-only validation utilities for FoxPro data paths, network ports, and LAN interfaces."""

from dataclasses import dataclass, field
import logging
from pathlib import Path
import socket
import struct
from typing import Dict, List, Optional, Tuple

logger = logging.getLogger("PYROJA.Validator")

REQUIRED_DBF_TABLES = ["ITEMMST.DBF", "NAMEMST.DBF", "SALETRN.DBF"]
OPTIONAL_DBF_TABLES = ["SALEMST.DBF", "COMPMST.DBF", "AREAMST.DBF", "TAXMST.DBF"]


@dataclass
class DbfFileInfo:
    name: str
    exists: bool = False
    record_count: int = 0
    size_bytes: int = 0
    readable: bool = False
    error: Optional[str] = None


@dataclass
class FolderValidationResult:
    valid: bool
    path: str
    error_message: Optional[str] = None
    missing_required: List[str] = field(default_factory=list)
    tables: Dict[str, DbfFileInfo] = field(default_factory=dict)


def inspect_dbf_header_readonly(file_path: Path) -> Tuple[int, int, bool, Optional[str]]:
    """Inspect FoxPro DBF header in strictly read-only binary mode.

    Returns:
        Tuple of (record_count, file_size_bytes, readable_bool, error_string)
    """
    if not file_path.is_file():
        return 0, 0, False, "File does not exist or is not a regular file"

    try:
        size = file_path.stat().st_size
        with open(file_path, "rb") as f:
            header = f.read(32)
            if len(header) < 32:
                return 0, size, False, "Corrupt or truncated DBF header (< 32 bytes)"

            # FoxPro DBF format:
            # Byte 0: FoxPro version/flag
            # Bytes 4..7: uint32 record count (little-endian)
            # Bytes 8..9: uint16 header length
            # Bytes 10..11: uint16 record length
            record_count = struct.unpack("<I", header[4:8])[0]
            header_len = struct.unpack("<H", header[8:10])[0]
            record_len = struct.unpack("<H", header[10:12])[0]

            if header_len == 0 or record_len == 0:
                return record_count, size, True, "Warning: Header or record length is 0"

            return record_count, size, True, None
    except PermissionError:
        return 0, 0, False, "Permission denied (unable to read file)"
    except Exception as exc:
        return 0, 0, False, f"Read error: {exc}"


def validate_foxpro_folder(path_str: str) -> FolderValidationResult:
    """Validate that the configured directory exists and contains required FoxPro DBFs.

    STRICT SAFETY GUARANTEE:
    This function performs strictly read-only inspection.
    It never writes, creates, locks, or modifies files in the target directory.
    """
    if not path_str or not path_str.strip():
        return FolderValidationResult(
            valid=False,
            path="",
            error_message="FoxPro folder path is empty. Please specify a valid folder path.",
        )

    folder_path = Path(path_str.strip())

    if not folder_path.exists():
        return FolderValidationResult(
            valid=False,
            path=str(folder_path),
            error_message=f"Directory does not exist: {folder_path}",
        )

    if not folder_path.is_dir():
        return FolderValidationResult(
            valid=False,
            path=str(folder_path),
            error_message=f"Path is a file, not a directory: {folder_path}",
        )

    # Build a case-insensitive map of files in the directory
    try:
        dir_files = {p.name.upper(): p for p in folder_path.iterdir() if p.is_file()}
    except PermissionError:
        return FolderValidationResult(
            valid=False,
            path=str(folder_path),
            error_message=f"Permission denied: cannot read directory {folder_path}",
        )
    except Exception as exc:
        return FolderValidationResult(
            valid=False,
            path=str(folder_path),
            error_message=f"Error accessing directory: {exc}",
        )

    tables: Dict[str, DbfFileInfo] = {}
    missing_required: List[str] = []

    # Check required tables
    for req in REQUIRED_DBF_TABLES:
        req_upper = req.upper()
        if req_upper in dir_files:
            file_path = dir_files[req_upper]
            rec_cnt, sz, readable, err = inspect_dbf_header_readonly(file_path)
            tables[req] = DbfFileInfo(
                name=req,
                exists=True,
                record_count=rec_cnt,
                size_bytes=sz,
                readable=readable,
                error=err,
            )
            if not readable:
                missing_required.append(f"{req} (unreadable: {err})")
        else:
            tables[req] = DbfFileInfo(
                name=req,
                exists=False,
                error="File not found in folder",
            )
            missing_required.append(req)

    # Check optional tables
    for opt in OPTIONAL_DBF_TABLES:
        opt_upper = opt.upper()
        if opt_upper in dir_files:
            file_path = dir_files[opt_upper]
            rec_cnt, sz, readable, err = inspect_dbf_header_readonly(file_path)
            tables[opt] = DbfFileInfo(
                name=opt,
                exists=True,
                record_count=rec_cnt,
                size_bytes=sz,
                readable=readable,
                error=err,
            )

    if missing_required:
        err_msg = (
            f"Missing required FoxPro table(s): {', '.join(missing_required)}. "
            f"Please ensure the folder contains the active financial year DBFs."
        )
        return FolderValidationResult(
            valid=False,
            path=str(folder_path),
            error_message=err_msg,
            missing_required=missing_required,
            tables=tables,
        )

    return FolderValidationResult(
        valid=True,
        path=str(folder_path),
        tables=tables,
    )


def is_port_available(port: int, host: str = "0.0.0.0") -> Tuple[bool, Optional[str]]:
    """Test if a given TCP port is available for binding.

    Returns:
        Tuple of (is_available: bool, error_message: Optional[str])
    """
    if not isinstance(port, int) or port < 1024 or port > 65535:
        return False, f"Invalid port {port}. Port must be an integer between 1024 and 65535."

    bind_host = "" if host == "0.0.0.0" else host
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        try:
            sock.bind((bind_host, port))
            return True, None
        except OSError as exc:
            return False, f"Port {port} is already in use by another service or application ({exc.strerror})."


def get_primary_lan_ip() -> str:
    """Determine the primary routable IPv4 address of this machine.

    Tries standard UDP connection test without sending data.
    Falls back to socket hostname lookup or 127.0.0.1.
    """
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            # Does not send actual traffic over the wire
            s.connect(("8.8.8.8", 80))
            ip = s.getsockname()[0]
            if ip and not ip.startswith("127."):
                return ip
    except Exception:
        pass

    try:
        hostname = socket.gethostname()
        for info in socket.getaddrinfo(hostname, None, socket.AF_INET):
            candidate = info[4][0]
            if candidate and not candidate.startswith("127."):
                return candidate
    except Exception:
        pass

    return "127.0.0.1"


def get_all_lan_ips() -> List[str]:
    """Return a list of non-loopback IPv4 addresses detected on this machine."""
    ips: List[str] = []
    primary = get_primary_lan_ip()
    if primary != "127.0.0.1":
        ips.append(primary)

    try:
        hostname = socket.gethostname()
        for info in socket.getaddrinfo(hostname, None, socket.AF_INET):
            candidate = info[4][0]
            if candidate and not candidate.startswith("127.") and candidate not in ips:
                ips.append(candidate)
    except Exception:
        pass

    if not ips:
        ips.append("127.0.0.1")
    return ips


def get_tablet_url(ip: str, port: int) -> str:
    """Format the tablet connection URL."""
    return f"http://{ip}:{port}"
