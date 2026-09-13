"""Windows Sync Service for PYROJA ↔ FoxPro integration."""

import pathlib


def _load_version() -> str:
    root_version = pathlib.Path(__file__).resolve().parent.parent.parent / "VERSION"
    if root_version.is_file():
        return root_version.read_text(encoding="utf-8").strip()
    return "0.1.0-alpha"


__version__ = _load_version()
