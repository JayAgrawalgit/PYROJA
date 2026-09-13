# Master Project Changelog: PYROJA Retail POS & FoxPro Sync System

## [1.0.0] - 2026-09-13

### Windows Sync Service Standalone Executable (`PYRO-Sync-Service/`)
- **Standalone 64-bit Windows Binary:** Packaged the entire Python FastAPI FoxPro Sync Service into a self-contained distribution folder `PYRO-Sync-Service/` containing `PYRO-Sync-Service.exe`.
- **Embedded Python 3.11.9 Engine:** Included official CPython 3.11 64-bit runtime (`python311.dll`, `python3.dll`, `python311.zip`) eliminating any need for target machines to install Python.
- **Embedded SQLite WAL Engine:** Bundled precompiled `sqlite3.dll` and `_sqlite3.pyd` for offline transaction safety and zero-locking concurrency.
- **Precompiled Binary Wheels:** Integrated Windows x86_64 wheels for FastAPI, Uvicorn, Pydantic, PyYAML, WebSockets, HTTPX, and Starlette.
- **MinGW-w64 PE Launcher:** Compiled custom native C console launcher (`PYRO-Sync-Service.exe`) that configures terminal titles, resolves application directories, and calls `Py_Main` in-process.
- **External Configuration:** Provided `config.json` for easy administration in Notepad (port, host, FoxPro data path, logging level).
- **Interactive Batch Script:** Created `start_sync_service.bat` with auto-IP detection for tablet pairing.
- **Ghost Product Exclusion:** Filtered discontinued/ghost records (`NAME` empty, `CQTY <= 0`, `SRATE <= 0`) from product sync and category badge counts.

### Android POS Tablet App
- **Clean Product Catalog UI:** Simplified product rows across catalog, search, and category views to show strictly `${p.name}` without technical metadata (pack, GST, inner box units).
- **Diagnostic Bar Removal:** Removed the legacy footer/diagnostic status bar cleanly across all screens (Catalog, Search, Cart, Quantity Dialog, Checkout).
- **Cache Invalidation:** Enforced Chromium WebView disk cache bypass (`LOAD_NO_CACHE`) in `MainActivity.java` to prevent stale UI assets.
- **Single Release APK:** Consolidated build pipeline to produce exactly one clean installable release APK (`tablet-app/dist/app-release.apk`).

### Documentation & Build System
- Added `EXECUTABLE_AUDIT.md`, `EXE_BUILD_REPORT.md`, `WINDOWS_DEPLOYMENT_GUIDE.md`, and `EXE_CHANGELOG.md`.
- Added Docker reproducible cross-compilation pipeline (`packaging/Dockerfile.dist_builder`, `packaging/build_windows_dist.sh`).
