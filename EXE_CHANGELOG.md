# Executable & Deployment Changelog: PYRO-Sync-Service

## Version 1.0.0 (2026-09-13)

### Added
- **Native 64-bit Windows PE Launcher (`PYRO-Sync-Service.exe`):**
  - Compiled using MinGW-w64 GCC (`x86_64-w64-mingw32-gcc`).
  - Embedded in-process CPython 3.11.9 runtime initialization via direct `Py_Main` entrypoint.
  - Dynamically sets console window title and working directory.
  - Standard command-line argument passthrough.
- **Self-Contained Embedded Python 3.11.9 Core:**
  - Official CPython Windows 64-bit runtime libraries (`python311.dll`, `python3.dll`).
  - Base standard library archive (`python311.zip`).
  - Precompiled Windows C-extensions (`_socket.pyd`, `_ssl.pyd`, `_sqlite3.pyd`, `_asyncio.pyd`, `_ctypes.pyd`).
  - Isolated search path specification (`python311._pth`).
- **Bundled Windows Binary Wheels (`site-packages/`):**
  - FastAPI 0.141.1, Uvicorn 0.52.4, Starlette 1.6.0.
  - Pydantic 2.13.5 & Pydantic-Core 2.46.5 (Windows `.pyd`).
  - PyYAML 6.0.3 (Windows `.pyd`).
  - WebSockets 17.1 (Windows `.pyd`).
  - HTTPX 0.28.1 and AnyIO 4.15.1.
- **External Configuration (`config.json`):**
  - Formatted JSON configuration allowing external editing of server port, host, FoxPro data path, and logging level.
- **Interactive Batch Launcher (`start_sync_service.bat`):**
  - Auto-detects local LAN IPv4 address for tablet pairing.
  - Prints clear status banner and interactive documentation URLs.
- **Reproducible Build Pipeline:**
  - `packaging/Dockerfile.dist_builder`: Debian Bookworm ARM64 cross-compilation environment.
  - `packaging/build_windows_dist.sh`: End-to-end automated distribution assembly script.
  - `packaging/verify_windows_deployment.sh`: Automated test suite simulating Windows runtime execution under Wine 9.0.

### Modified
- **`sync-service/app/config.py`:**
  - Added support for detecting `sys.frozen` and executable directory.
  - Added priority loader for `config.json` before falling back to `config.yaml`.
  - Added path normalization for relative FoxPro and SQLite database paths.
- **`sync-service/app/logging_config.py`:**
  - Added support for executable directory resolution when frozen.
  - Added automatic parent directory creation (`log_path.parent.mkdir(parents=True, exist_ok=True)`) to ensure `logs/` directory exists.
- **`sync-service/app/main.py`:**
  - Updated `uvicorn.run()` to pass the instantiated `app` object directly instead of a dynamic import string.
  - Added `multiprocessing.freeze_support()` for Windows process initialization safety.
