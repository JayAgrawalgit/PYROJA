# PYROJA

[![Release](https://img.shields.io/badge/release-v1.0.0-blue.svg)](https://github.com/JayAgrawalgit/PYROJA/releases/tag/v1.0.0)
[![Target OS](https://img.shields.io/badge/Windows-10%20%7C%2011%20%7C%20Server-0078D6.svg?logo=windows)](https://microsoft.com/windows)
[![Android](https://img.shields.io/badge/Android-POS%20Tablet%208.0%2B-3DDC84.svg?logo=android)](https://developer.android.com)
[![License](https://img.shields.io/badge/license-Proprietary-red.svg)](#license)

**PYROJA** is a production-grade retail Point of Sale (POS) and local LAN synchronization system bridging modern touchscreen Android tablets with legacy **Visual FoxPro 6.0 (FAVWIN)** retail ERP engines.

---

## Architecture Overview

```
 ┌─────────────────────────────────────────────────────────┐
 │                  Android POS Tablet                     │
 │  • Touchscreen Order Entry & Master Data Browser        │
 │  • Pure Product Description Display (Zero Metadata)     │
 │  • Offline IndexedDB Queue with Idempotency Protection  │
 └────────────────────────────┬────────────────────────────┘
                              │
                    Local Wi-Fi / LAN (HTTP)
                              │
                              ▼
 ┌─────────────────────────────────────────────────────────┐
 │               PYROJA Windows Sync Service               │
 │  • Standalone Windows PE Executable (PYROJA.exe)        │
 │  • Zero Python / Zero ODBC Installation Required        │
 │  • High-Performance Zero-Locking Binary DBF Engine      │
 │  • SQLite WAL Mode Order Ledger & Audit Log             │
 └────────────────────────────┬────────────────────────────┘
                              │
                     Shared File Access
                              │
                              ▼
 ┌─────────────────────────────────────────────────────────┐
 │                 Visual FoxPro 6.0 ERP                   │
 │  • ITEMMST.DBF (Inventory Catalog & Price Tiers)        │
 │  • NAMEMST.DBF (Customer Ledger & Account Balances)     │
 │  • COMPMST.DBF, AREAMST.DBF, TAXMST.DBF Masters         │
 └─────────────────────────────────────────────────────────┘
```

---

## Key Features

1. **100% Standalone Windows Executable:**
   - Bundles an embedded 64-bit CPython 3.11.9 runtime with precompiled binary wheels (`FastAPI`, `Uvicorn`, `Pydantic`, `PyYAML`, `WebSockets`).
   - Runs out of the box on Windows 10, Windows 11, and Windows Server 2016+ without requiring Python, pip, or Visual C++ runtimes.
2. **Zero-Locking Binary FoxPro Reader:**
   - Direct binary decoding of FoxPro DBF tables (`ITEMMST`, `NAMEMST`, `COMPMST`, `AREAMST`, `TAXMST`) with zero table locking.
   - Operates concurrently with active legacy FoxPro desktop instances without causing file lock collisions or share violations.
3. **Ghost Product & Discontinued Record Filtering:**
   - Automatically detects and filters ghost/placeholder records (empty names, stock $\le 0$, rate $\le 0$) from sync outputs and category badge totals.
4. **Resilient Offline Order Queueing:**
   - Orders submitted from POS tablets are persisted into an ACID-compliant SQLite WAL database (`sync_service.sqlite3`) with draft ID deduplication and idempotency protection.
5. **Pure Product Description UI:**
   - Tablet catalog and search interfaces display clean, uncluttered product names `${p.name}` without technical metadata (pack sizes, GST rates, inner unit counts).
6. **External Editable Configuration:**
   - Server host, port, FoxPro data directory, and logging levels can be configured directly in `config.json` using Notepad without rebuilding binaries.

---

## System Requirements

| Component | Requirements |
| :--- | :--- |
| **Server / Host Computer** | Windows 10, 11, or Windows Server 2016+ (64-bit x86_64) |
| **Tablet Hardware** | Android 8.0 (Oreo) or higher, 10" or 11" display recommended |
| **Network** | Dedicated Local Area Network (Wi-Fi 5 or Wi-Fi 6 router) |
| **Software Dependencies** | None. Completely self-contained. |

---

## Installation & Deployment

### Windows Host Deployment

1. Download the latest `release/` package or extract the deployment folder `PYRO-Sync-Service/` to your target directory (e.g. `C:\PYROJA`).
2. Open `config.json` in Notepad and verify your FoxPro fiscal directory:
   ```json
   {
     "server": {
       "host": "0.0.0.0",
       "port": 8080
     },
     "foxpro": {
       "data_path": "C:\\FAVWIN\\D2627",
       "active_fiscal_year": "D2627"
     },
     "logging": {
       "level": "INFO",
       "file": "logs/sync_service.log"
     }
   }
   ```
3. Run `start_pyroja.bat` (or `start_sync_service.bat`).
4. The console window will display the detected LAN IP address (e.g. `http://192.168.1.50:8080`) and table health statuses.

### Windows Firewall Configuration

Allow inbound traffic on port 8080 by running Command Prompt as Administrator:
```cmd
netsh advfirewall firewall add rule name="PYROJA" dir=in action=allow protocol=TCP localport=8080
```

### Android Tablet Setup

1. Connect the tablet to the store Wi-Fi network.
2. Install `PYROJA-Tablet-Release.apk` (or build via `npm run build:apk` in `tablet-app/`).
3. Launch PYROJA on the tablet.
4. Set the Sync URL to: `http://<WINDOWS_COMPUTER_IP>:8080`.
5. Tap **Sync Now** to download catalog and customer balances.

---

## Environment Variables

PYROJA supports both primary `PYROJA_*` and backward-compatible `SYNC_*` variables:

| Primary Variable | Legacy Variable (Deprecated) | Description | Default |
| :--- | :--- | :--- | :--- |
| `PYROJA_SERVER_HOST` | `SYNC_SERVER_HOST` | IP interface to bind server | `0.0.0.0` |
| `PYROJA_SERVER_PORT` | `SYNC_SERVER_PORT` | TCP port number | `8080` |
| `PYROJA_FOXPRO_DATA_PATH`| `SYNC_FOXPRO_DATA_PATH` | Fiscal data folder path | `../legacy-software-extracted/FAVWIN/D2627` |
| `PYROJA_DATABASE_PATH` | `SYNC_DATABASE_PATH` | SQLite state database file | `sync_service.sqlite3` |
| `PYROJA_LOG_LEVEL` | `SYNC_LOG_LEVEL` | Logging verbosity (`INFO`, `DEBUG`) | `INFO` |
| `PYROJA_CONFIG_PATH` | `SYNC_CONFIG_PATH` | Path to custom config file | `config.json` / `config.yaml` |

---

## Running Locally for Development

### Sync Service (Python)
```bash
cd sync-service
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --host 0.0.0.0 --port 8080 --reload
```

### Tablet POS Web Assets
```bash
cd tablet-app
npm install
npm run build
npm run sync
```

---

## Verification & Health Endpoints

- **Interactive API Documentation:** `http://localhost:8080/docs`
- **System Health & DBF Table Status:** `http://localhost:8080/api/health`
- **Product Catalog Sync:** `http://localhost:8080/api/sync/products`
- **Customer Master Sync:** `http://localhost:8080/api/sync/customers`
- **Order Queueing:** `POST http://localhost:8080/api/orders`

---

## Troubleshooting

- **Table Status `MISSING`:** Check `data_path` in `config.json`. Ensure backslashes are escaped (`C:\\FAVWIN\\D2627`).
- **Tablet Network Error:** Ensure the Windows machine has a static IP or DHCP reservation and that port 8080 is open in Windows Firewall.
- **Port Conflict:** If port 8080 is used by another service, change `"port": 8085` in `config.json` and restart `start_pyroja.bat`.

---

## Documentation & Architecture Guides

- **Operator Deployment:** [`WINDOWS_DEPLOYMENT_GUIDE.md`](WINDOWS_DEPLOYMENT_GUIDE.md) — Production setup for Windows host and firewall.
- **Developer Workflow:** [`DEVELOPMENT_WORKFLOW.md`](DEVELOPMENT_WORKFLOW.md) — Engineering standards, tests, and automated commit pipeline.
- **Repository Audit:** [`ARTIFACT_AUDIT.md`](ARTIFACT_AUDIT.md) — Forensic audit and artifact census report.
- **System Specifications:** [`docs/specs/`](docs/specs/) — Visual FoxPro table relationships, CDX index models, import workflows, and catalog architecture.
- **Product Packaging Rules:** [`docs/packaging/`](docs/packaging/) — Business review worksheets, risk register, and empirical sales analysis.
- **Historical Archive:** [`docs/archive/`](docs/archive/) — Milestone audits, build reports, and verification evidence.

---

## License

Proprietary — All rights reserved.
