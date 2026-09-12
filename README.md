# PYROJA 🔥

**High-Throughput Offline-First Android Tablet POS & Visual FoxPro Sync System**  
*Tailored for RAM FATAKA CENTER Wholesale Fireworks Billing Operations*

---

## 1. Overview & Business Problem Solved

During the peak Diwali festive rush, fireworks wholesalers face extreme transaction volume with rapid counter sales, high-value bulk purchases, and continuous customer flow. 

Historically, **RAM FATAKA CENTER** operated on a single legacy **Visual FoxPro 6.0 (`FAVWIN`)** back-office billing terminal. This legacy setup introduced critical operational bottlenecks:
- **Cashier Queue Bottlenecks:** Multiple showroom salesmen had to queue up at a single terminal to generate estimates, causing 30–45 minute order fulfillment delays.
- **Terminal Lockouts & Concurrency Issues:** FoxPro `.DBF` files could not support concurrent multi-user write access without file locks or database corruption risks.
- **Wholesale Pack Quantity Friction:** Firecracker items are packaged in bulk (boxes of 10, 25, 50, 100, 1000). Standard POS systems designed for single-item retail could not handle quick wholesale order entry or enforce pack-size multiples on the floor.
- **Unreliable Network Resilience:** Showroom connectivity drops during peak hours would freeze thin-client POS software, halting billing entirely.

### The PYROJA Solution
**PYROJA** solves these challenges by untethering sales operators with rugged Android tablets backed by an offline-first architecture and a zero-locking local Windows Sync Service:
1. **Multi-Operator Floor Billing:** Salesmen walk the showroom with tablets, opening independent draft carts for multiple buyers simultaneously.
2. **Offline-First Resilience:** The full catalog (3,000+ items across 50+ categories) is cached locally in IndexedDB/SQLite on the tablet. Billing continues with zero latency even if WiFi drops out entirely.
3. **Wholesale Quantity Steppers:** Dedicated direct numeric quantity entry modals with quick-step buttons (`-10`, `-1`, `+1`, `+10`) and dynamic pack multiple enforcement.
4. **Zero-Locking Windows Sync:** A lightweight Python FastAPI service reads master data from FoxPro without locking files, validates incoming orders, and stages them safely into FoxPro's Estimate (`E`) billbook.

---

## 2. System Architecture

```text
 ┌────────────────────────────────────────────────────────────────────────┐
 │                           PYROJA SYSTEM                                │
 └───────────────────────────────────┬────────────────────────────────────┘
                                     │
           ┌─────────────────────────┴─────────────────────────┐
           ▼                                                   ▼
 ┌───────────────────────────┐                       ┌───────────────────┐
 │   Android Tablet POS      │                       │  Sync Service     │
 │   (Capacitor + Web View)  │                       │  (FastAPI on LAN) │
 └─────────────┬─────────────┘                       └─────────┬─────────┘
               │                                               │
   Offline     │ HTTP REST                                Zero │ Direct DBF
   IndexedDB   │ (WiFi LAN :8080)                         Lock │ Binary Read
               │                                               │
               ▼                                               ▼
 ┌───────────────────────────┐                       ┌───────────────────┐
 │ Local Tablet Storage      │                       │ Legacy Visual     │
 │ • 3,019 Products Cached   │                       │ FoxPro 6.0        │
 │ • Multi-Account Drafts    │                       │ (FAVWIN D2627)    │
 │ • Offline Sync Queue      │                       │ • ITEMMST.DBF     │
 └───────────────────────────┘                       │ • COMPMST.DBF     │
                                                     │ • BILLBOOK.DBF    │
                                                     └───────────────────┘
```

### Component Details

#### A. Android Tablet POS (`tablet-app/`)
- **Runtime:** Android Native Wrapper via **Capacitor 8.5.1**, targeting Android 7.0+ (API 24 to 36). Tested on Google Pixel Tablet (Android 15).
- **Frontend Stack:** HTML5, Tailwind CSS, Vanilla JavaScript (`app.js`, `index.html`).
- **Data Layer:** IndexedDB (`PYROJA`, with automated safe migration from legacy `PyroWholesalePOS`) backed by Android WebView SQLite in Write-Ahead Logging (WAL) mode.
- **Identifier Protection:** Native package name **`com.pyrowholesale.pos`** is preserved to allow seamless in-place APK updates (`adb install -r`) without loss of local drafts.

#### B. Sync Service (`sync-service/`)
- **Runtime:** Python 3.10+ (FastAPI, Uvicorn, SQLite3 WAL).
- **FoxPro Integration:** Custom pure-Python zero-locking DBF reader (`app/db/dbf_reader.py`) reading binary tables without external ODBC drivers or locking table headers.
- **Validation Engine:** Enforces customer validity, product code existence, stock levels, and packaging multiples (`qty % pack_qty == 0`).
- **Security & Network:** Operates entirely within the local showroom subnet (e.g. `http://192.168.1.X:8080`).

#### C. Legacy FoxPro Database (`FAVWIN/D2627`)
- **Master Tables:**
  - `ITEMMST.DBF`: Product catalog, rates, pack units, closing quantities (`CQTY`).
  - `COMPMST.DBF`: Fireworks brand and manufacturer names.
  - `ARTH.DBF`: Customer accounts and credit terms.
  - `BILLBOOK.DBF`: Active billbooks (`E` = Estimate series).
- **Target Series:** Tablet drafts are imported exclusively into the Estimate series (`E`), leaving audited GST tax invoices isolated.

---

## 3. Product Roadmap (Alpha → Beta → Gamma)

| Phase | Status | Key Milestones & Capabilities |
| :--- | :---: | :--- |
| **Alpha** | ✅ Complete | • Zero-locking master data reader (`ITEMMST.DBF`, `COMPMST.DBF`).<br>• Local SQLite state store with WAL mode.<br>• Offline IndexedDB cache on Android tablet.<br>• Single-cart billing and draft synchronization.<br>• Android emulator validation report. |
| **Beta** | 🚀 **Current** | • **Multi-Account Draft Billing:** Independent tabs for Cash A/C and wholesale retailers with separate carts.<br>• **Wholesale Quantity Steppers:** Direct numeric input modal with `-10`/`+10` quick steps and pack-size multiples.<br>• **Category & Subcategory Filters:** Dynamic pack-type pills (`PKT`, `BOX`, `PCS`, `BAG`, `ROLL`, `TIN`).<br>• **Server Configuration Modal:** Real-time LAN connection test with latency measurement.<br>• **Production APK:** `tablet-app/dist/pyroja-pos-debug.apk` tested on live tablet. |
| **Gamma** | 🔮 Planned | • **Two-Way Live Stock Decrement:** Real-time stock reservation across tablets.<br>• **Thermal Printing:** Direct Bluetooth 80mm ESC/POS receipt generation (`BT-80P READY`).<br>• **Multi-Tablet Concurrency Conflict Resolution:** Cloud-assisted conflict handling for simultaneous cashier checkouts.<br>• **Automated Daily Backups:** Incremental snapshotting of FoxPro data directories. |

---

## 4. Local Development Setup

### Prerequisites
- **Node.js:** v18.0.0 or higher
- **Python:** v3.10 or higher
- **Android Studio & SDK:** API Level 35 SDK + Build Tools
- **Java:** JDK 21 (OpenJDK / Android Studio JBR)

### 1. Sync Service Setup (macOS / Linux / Windows)
```bash
cd sync-service

# Create and activate Python virtual environment
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the test suite (26 integration tests)
pytest tests/ -v

# Launch local development server with auto-reload
uvicorn app.main:app --host 0.0.0.0 --port 8080 --reload
```
Interactive API documentation will be available at `http://localhost:8080/docs`.

### 2. Tablet POS Setup
```bash
cd tablet-app

# Install Capacitor CLI and dependencies
npm install

# Build web distribution and copy to www/
npm run build

# Synchronize web assets with Android native project
npx cap sync android
```

---

## 5. Building the Android APK

### Quick One-Step Build
```bash
cd tablet-app
export ANDROID_HOME="$HOME/Library/Android/sdk"
export JAVA_HOME="/Applications/Android Studio.app/Contents/jbr/Contents/Home"
npm run build:apk
```

### Manual Step-by-Step Compilation
```bash
cd tablet-app

# 1. Bundle web assets
npm run sync

# 2. Compile debug APK using Gradle
cd android
./gradlew assembleDebug --no-daemon

# 3. Copy compiled APK to project dist folder
cp app/build/outputs/apk/debug/app-debug.apk ../dist/pyroja-pos-debug.apk
```

### Generated Binaries
- **Primary Release APK:** [`tablet-app/dist/pyroja-pos-debug.apk`](tablet-app/dist/pyroja-pos-debug.apk) *(8.68 MB)*
- **Legacy Symlink APK:** [`tablet-app/dist/pyrowholesale-pos-debug.apk`](tablet-app/dist/pyrowholesale-pos-debug.apk) *(8.68 MB)*

### Deploying to Connected Tablet via ADB
```bash
adb install -r "tablet-app/dist/pyroja-pos-debug.apk"
adb shell am start -n com.pyrowholesale.pos/.MainActivity
```

---

## 6. Windows Production Deployment

To run the PYROJA Sync Service on the Windows billing computer hosting Visual FoxPro:

### Step 1: Place Files on Billing Server
Copy the `sync-service/` folder to `C:\PYROJA\sync-service`. Ensure the FoxPro database path is accessible (e.g. `C:\FAVWIN\D2627`).

### Step 2: Configure Environment
Edit `C:\PYROJA\sync-service\config.yaml`:
```yaml
server:
  host: "0.0.0.0"
  port: 8080

foxpro:
  data_dir: "C:\\FAVWIN\\D2627"
  billbook_code: "E "

database:
  sqlite_path: "sync_service.sqlite3"
```

### Step 3: Configure Windows Firewall
Open port 8080 for tablet communication over the showroom WiFi:
```powershell
New-NetFirewallRule -DisplayName "PYROJA Sync Service (Port 8080)" -Direction Inbound -LocalPort 8080 -Protocol TCP -Action Allow
```

### Step 4: Launch the Service
Double-click `sync-service/scripts/start_server.bat` or run:
```cmd
cd C:\PYROJA\sync-service
.venv\Scripts\python.exe -m uvicorn app.main:app --host 0.0.0.0 --port 8080
```
Verify the service is active from any browser on the network: `http://<WINDOWS_SERVER_IP>:8080/api/health`.

---

## 7. Database Sync Flow

```text
  [FoxPro Tables] 
         │ 
         │ 1. Zero-locking binary read via dbfread
         ▼
  [FastAPI Service]
         │
         │ 2. Stage to internal SQLite in WAL mode
         ▼
  [JSON Master API] ──(WiFi GET)──► [Tablet IndexedDB]
  • /api/sync/products               • Stores 3,019 items
  • /api/sync/customers              • Enforces pack multiples

─────────────────────────────────────────────────────────────

  [Tablet Draft Cart]
         │
         │ 3. Operator hits "Confirm & Dispatch Draft"
         ▼
  [Local Sync Queue]
         │
         │ 4. POST /api/orders (with Idempotency Key)
         ▼
  [Sync Service Queue]
         │
         │ 5. Validates customer, products, pack multiples
         ▼
  [FoxPro Staging / DBF Export]
         │
         │ 6. Appends to BILLBOOK (Series E - Estimate)
         ▼
  [FAVWIN Billing Complete]
```

---

## 8. Offline Mode Behavior

1. **Optimistic Local Storage:** All product catalogs, categories, and customer master accounts are stored in the tablet's local IndexedDB (`PYROJA`).
2. **Crash & Restart Protection:** If the tablet runs out of battery or is rebooted, all active customer drafts remain intact and load automatically upon restart.
3. **Disconnected Checkout:** When WiFi is unavailable, tapping **"Confirm & Dispatch Draft"** queues the order in the tablet's local `sync_queue` store.
4. **Auto-Reconnection Sync:** When connection to the LAN server is re-established, the background sync worker flushes queued orders to the server automatically.
5. **No Double Billing:** Each draft is assigned a UUID-based draft identifier (e.g. `TAB01-1048`), ensuring that retried sync packets are deduplicated by the server idempotency filter.

---

## 9. Semantic Versioning & Release Management

PYROJA follows strict [Semantic Versioning (SemVer 2.0.0)](https://semver.org/):
```text
MAJOR.MINOR.PATCH[-PRERELEASE]
Example: 0.1.0-alpha
```

### Single Source of Truth (`VERSION`)
The version is governed by a single root file: [`VERSION`](VERSION).

All components dynamically consume this single source of truth without manual code duplication:
- **Tablet POS Header:** Reads `VERSION` via `tablet-app/scripts/sync-version.js` (written to `version.js` / `window.APP_VERSION`), rendering dynamically in the top-left UI header:
  ```text
  🔥 PYROJA v0.1.0-alpha
  ```
- **Sync Service API:** Reads `VERSION` on startup in `sync-service/app/__init__.py`, exposing the version in `GET /` and `GET /api/health`.
- **Node Manifest:** Linked to `tablet-app/package.json` `"version"`.

### Bumping a Release
1. Update the version string in the root [`VERSION`](VERSION) file (e.g. `0.2.0-beta`).
2. Run the automated release pipeline:
   ```bash
   ./scripts/workflow.sh "chore(release): bump version to 0.2.0-beta" --build-apk
   ```
3. The script automatically synchronizes web assets, updates the UI badge, compiles the release APK, runs backend tests, and commits with Conventional Commits.

---

## 10. Developer & Git Workflow

All contributors must adhere to the automated development workflow:
- **Zero-Broken-Build Policy:** Never commit failing code.
- **Conventional Commits:** Format must be `<type>(<scope>): <subject>`.
- **Automated Workflow Script:**
  ```bash
  # Validates tests, stages files, commits, and pushes (if remote exists)
  ./scripts/workflow.sh "feat(cart): add instant pack multiplier"
  ```

For complete workflow rules, refer to [DEVELOPMENT_WORKFLOW.md](DEVELOPMENT_WORKFLOW.md).

---

## 11. Troubleshooting

### 1. Tablet Shows "Connecting..." or Fails to Sync
- **Cause:** Tablet cannot reach Windows host over WiFi or server IP changed.
- **Solution:** Tap the **Settings (gear)** icon in the top header to open the **Server Configuration** modal. Enter the Windows PC's current IP address (e.g. `http://192.168.1.34:8080`) and tap **Test Connection**. Once latency is displayed, tap **Save**.

### 2. Product Grid Stuck on "Loading FoxPro product catalog..."
- **Cause:** Initial master sync has not occurred or IndexedDB is empty.
- **Solution:** Verify server connectivity, then tap **PULL DBF MASTERS** in the top header bar to trigger a full refresh.

### 3. Order Submission Rejected with 422 Unprocessable Content
- **Cause:** Pack multiple mismatch (e.g. ordering 15 units of an item that has a pack quantity of 20).
- **Solution:** Use the wholesale quantity stepper modal to select a valid multiple.

### 4. Windows Sync Service Shows "File In Use" / Error 32
- **Cause:** Exclusive lock by FoxPro during month-end indexing.
- **Solution:** Ensure `dbf_reader.py` opens files with shared read access (`rb`). Never open `.DBF` files in write mode while `FAVWIN.EXE` is running.

---

## 11. Screenshots & Visual Artifacts

| View | Screenshot Reference | Description |
| :--- | :---: | :--- |
| **Live POS Interface** | ![Live UI](file:///Users/jayagrawal/.gemini/antigravity/brain/a1401fd8-be5e-4dab-bd21-a1c8c38cdffe/pyroja_app_running_emulator.png) | High-density wholesale POS running on Android tablet emulator with active drafts. |
| **In-App Header** | ![Header](file:///Users/jayagrawal/.gemini/antigravity/brain/a1401fd8-be5e-4dab-bd21-a1c8c38cdffe/pyroja_header_screenshot.png) | Fire flame icon, coral PYROJA wordmark, and clean compact navigation. |
| **Android Launcher** | ![Launcher](file:///Users/jayagrawal/.gemini/antigravity/brain/a1401fd8-be5e-4dab-bd21-a1c8c38cdffe/pyroja_launcher_screenshot.png) | System app drawer displaying the PYROJA application launcher label. |

*(For detailed architectural decisions and audit reports, see [branding_migration_report.md](file:///Users/jayagrawal/.gemini/antigravity/brain/a1401fd8-be5e-4dab-bd21-a1c8c38cdffe/branding_migration_report.md) and [beta_readiness_report.md](file:///Users/jayagrawal/.gemini/antigravity/brain/a1401fd8-be5e-4dab-bd21-a1c8c38cdffe/beta_readiness_report.md)).*
