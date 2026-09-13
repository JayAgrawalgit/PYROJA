# Master Project Changelog: PYROJA Retail POS & FoxPro Sync System

All notable changes to the **PYROJA** system will be documented in this file.
This project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [1.0.0] - 2026-09-14

### Unified Branding & Standardization
- **Brand Consolidation:** Standardized project branding to **PYROJA** across all ecosystem layers:
  - Synchronized version across root `VERSION` (1.0.0), `sync-service` FastAPI metadata (`PYROJA v1.0.0`), and Android POS app (`1.0.0`, version code 1).
  - Modernized root `README.md` and distribution guides to feature consistent PYROJA architecture, ASCII schematics, and operational workflows.
- **Dual Environment Variable Support:** Enhanced configuration loader to support primary `PYROJA_*` environment variables (`PYROJA_HOST`, `PYROJA_PORT`, `PYROJA_FOXPRO_DATA_DIR`, `PYROJA_LOG_LEVEL`, `PYROJA_DB_PATH`, `PYROJA_LOG_PATH`) with backward-compatible fallback to legacy `SYNC_*` variables.
- **Operational File Path Continuity:** Preserved default operational paths `logs/sync_service.log` and SQLite database `sync_service.sqlite3` to ensure zero disruption to existing monitoring or deployment scripts.

### Windows Sync Service Standalone Distribution (`release/`)
- **Zero-Dependency 64-bit Distribution:** Packaged the entire Python FastAPI FoxPro Sync Service into a self-contained, turnkey distribution package ready for production deployment without requiring Python, pip, or Visual C++ redistributable installation.
- **Multi-Binary Launchers:** Provided compiled native C MinGW-w64 launchers:
  - `PYROJA.exe` & `PYROJA-Sync-Service.exe`: Unified brand launchers for operator clarity and process identification.
  - `PYRO-Sync-Service.exe`: Maintained legacy binary name for seamless drop-in backwards compatibility with existing shortcuts and startup scripts.
- **Embedded Python 3.11 Runtime:** Bundled official CPython 3.11 64-bit runtime engine (`python311.dll`, `python3.dll`, `python311.zip`) and precompiled Windows binary wheels.
- **Embedded SQLite WAL Engine:** Bundled precompiled `sqlite3.dll` and `_sqlite3.pyd` configured with Write-Ahead Logging (WAL) mode for concurrency and atomic FoxPro queue processing.
- **External Configuration & Automation:**
  - Shipped `config.sample.json` and `config.json` for straightforward editing in Notepad.
  - Provided `start_pyroja.bat` and `start_sync_service.bat` with automated local IP detection for effortless tablet pairing.
- **Ghost Product Exclusion:** Hardened sync pipeline to filter out ghost/discontinued placeholder records (`NAME` empty, `CQTY <= 0`, `SRATE <= 0`) from product listings and category badge counts.

### Android POS Tablet App
- **Product Display Simplification:** Enforced strict product description display across all catalog, search, and category views, showing strictly `${p.name}` without secondary technical metadata (pack size, GST, inner box units, rate types).
- **Diagnostic Bar Removal:** Decommissioned and cleanly removed the bottom diagnostic/status bar (previously showing storage mode and billbook series) across all screens (Catalog, Search, Cart, Quantity Dialog, Checkout) with zero layout shifts or orphaned event handlers.
- **WebView Cache Invalidation:** Configured Android WebView with `LOAD_NO_CACHE` in `MainActivity.java` to prevent stale UI bundle caching across tablet updates.
- **Single Release APK Output:** Consolidated Android Gradle build pipeline to generate exactly one verified release artifact (`tablet-app/dist/app-release.apk` / `app-release.apk`).

### Verification & Release Tooling
- **Reproducible Build Pipeline:** Added Docker containerization scripts (`packaging/Dockerfile.dist_builder`, `packaging/build_windows_dist.sh`) enabling reproducible cross-compilation of Windows binaries on any environment.
- **Automated Test Coverage:** Verified 100% test pass rate across unit and integration test suites in `sync-service/tests/test_api.py`.
