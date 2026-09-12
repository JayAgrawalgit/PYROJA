# Production Deployment Guide: Android Tablet & Windows Sync Service

**System:** PYROJA POS ↔ Visual FoxPro 6.0 Integration  
**Store:** RAM FATAKA CENTER, Ghatanji  
**Target Hardware:**
- **Primary Billing PC:** Windows 10/11 Pro (hosting `\FAVWIN\` and `sync-service`)
- **POS Terminals:** 10–11" Android Tablets (Android 10+) connected via local Wi-Fi LAN

---

## 1. Local Network & Wi-Fi Configuration

To ensure uninterrupted communication across the showroom, warehouse, and billing counter:

```
                          +-------------------------------+
                          |    Shop Wi-Fi Router (LAN)    |
                          |      Subnet: 192.168.1.0/24   |
                          +-------------------------------+
                                   /             \
                                  /               \
       +----------------------------+   +----------------------------+
       |   Windows Billing PC       |   |   Android POS Tablets      |
       |   Static IP: 192.168.1.100 |   |   DHCP: 192.168.1.101..120 |
       |   Sync Service: Port 8080  |   |   Offline SQLite / PWA     |
       +----------------------------+   +----------------------------+
```

### 1.1 Router Setup Checklist
1. Connect Billing PC via Ethernet (recommended) or dedicated 5GHz Wi-Fi.
2. In Router Admin Settings (`192.168.1.1`), assign a **DHCP Static Reservation** to the Billing PC MAC address:
   - **IP Address:** `192.168.1.100`
   - **Subnet Mask:** `255.255.255.0`
3. Configure Wi-Fi SSID with WPA2/WPA3 encryption (e.g. `RAM_FATAKA_POS`).
4. Ensure **AP Isolation** is **DISABLED** on the router so tablets can communicate with the PC.

---

## 2. Windows Sync Service Deployment (Billing PC)

### 2.1 Prerequisites
- Windows 10 or 11 (64-bit).
- Python 3.11 or higher installed. During Python setup, ensure **"Add python.exe to PATH"** is checked.
- Administrative access on the PC.

### 2.2 Installation Steps

1. Copy the `sync-service/` folder to the target directory:
   ```cmd
   C:\FAVWIN\sync-service\
   ```
2. Open **Command Prompt as Administrator**:
   ```cmd
   cd C:\FAVWIN\sync-service
   ```
3. Create the dedicated Python virtual environment:
   ```cmd
   python -m venv .venv
   ```
4. Activate virtual environment and install production packages:
   ```cmd
   .venv\Scripts\activate
   pip install -r requirements.txt
   ```
5. Configure `config.yaml`:
   ```yaml
   server:
     host: "0.0.0.0"
     port: 8080
     cors_origins: ["*"]

   foxpro:
     # Exact path to the active fiscal year directory
     data_path: "D:\\FAVWIN\\D2627"
     active_fiscal_year: "D2627"

   database:
     path: "sync_service.sqlite3"

   cache:
     ttl_seconds: 30
     validate_mtime: true

   logging:
     level: "INFO"
     file: "sync_service.log"
   ```

### 2.3 Open Windows Defender Firewall Port
Allow incoming connections on port 8080 from the local subnet:
```cmd
netsh advfirewall firewall add rule name="PYROJA Sync Port 8080" dir=in action=allow protocol=TCP localport=8080 profile=private,domain
```

### 2.4 Service Verification
Start the service in interactive test mode:
```cmd
scripts\start_server.bat
```
Open a web browser on the PC and test:
- `http://localhost:8080/api/health`
Expected response:
```json
{
  "status": "HEALTHY",
  "version": "1.0.0",
  "active_fiscal_year": "D2627",
  "database": { "is_healthy": true, "journal_mode": "WAL" },
  "tables": {
    "ITEMMST.DBF": { "exists": true, "record_count": 3020 },
    "NAMEMST.DBF": { "exists": true, "record_count": 883 }
  }
}
```

### 2.5 Run as Permanent Windows Service (Auto-Start on Boot)
Using **NSSM (Non-Sucking Service Manager)**:
1. Download `nssm.exe` and copy it to `C:\Windows\System32\`.
2. Run in Administrator Command Prompt:
   ```cmd
   nssm install PyroSyncService "C:\FAVWIN\sync-service\.venv\Scripts\python.exe" "-m uvicorn app.main:app --host 0.0.0.0 --port 8080"
   nssm set PyroSyncService AppDirectory "C:\FAVWIN\sync-service"
   nssm set PyroSyncService Start SERVICE_AUTO_START
   nssm set PyroSyncService AppStdout "C:\FAVWIN\sync-service\service_stdout.log"
   nssm set PyroSyncService AppStderr "C:\FAVWIN\sync-service\service_stderr.log"
   nssm start PyroSyncService
   ```

---

## 3. Android Tablet POS Deployment

### 3.1 Option A: Chrome PWA Kiosk Deployment (Fastest, Zero Build)
1. Connect the Android tablet to the store Wi-Fi (`RAM_FATAKA_POS`).
2. Open **Google Chrome** on the tablet.
3. In Chrome address bar, navigate to:
   ```
   http://192.168.1.100:8080/tablet/
   ```
   *(Or serve the `tablet-app/` directory via a static file server or host on port 8080)*
4. Tap the **Chrome 3-dot menu** $\to$ **"Add to Home screen"** / **"Install app"**.
5. Name the shortcut: **PYRO POS**.
6. An icon will appear on the Android home screen.
7. Open **Settings $\to$ Security $\to$ App Pinning** on Android:
   - Pin the PYRO POS app to lock staff into POS presentation mode.

### 3.2 Option B: Native Android APK (Capacitor / Android Studio)
For a standalone `.apk` installation:
```bash
# In tablet-app directory:
npm init -y
npm install @capacitor/core @capacitor/cli @capacitor/android
npx cap init "PYROJA" "com.pyrowholesale.pos" --web-dir .
npx cap add android
npx cap copy
npx cap open android
```
Build signed APK in Android Studio and transfer to tablets via USB/MDM.

---

## 4. Daily Operational Workflow

### 4.1 Morning Routine (Showroom Opening)
1. Turn on Billing PC. Verify Windows Service is running.
2. Power on Android tablets.
3. Open PYRO POS app. Observe the top indicator pill:
   - 🟢 `ONLINE (LAN 8080)` confirms connection.
4. Tap **"PULL DBF MASTERS"**:
   - Downloads 3,019 products and 883 customer accounts from FoxPro directly into tablet SQLite storage.

### 4.2 Order Capture & Showroom Sales
1. Tap customer tab (e.g. `CASH A/C` or search wholesale party `00688`).
2. Search products by 5-digit code (`00013`, `01989`, `06122`) or product name.
3. Use stepper (`+` / `-`) or keypad. Quantities adhere to pack rules (`QIB`).
4. Active cart dynamically updates subtotal, 18% GST, and grand total.
5. Tap **"Confirm & Dispatch Draft"**:
   - Order is validated, assigned UUID `idempotency_key`, and queued.
   - If Wi-Fi is reachable: uploaded instantly to Sync Service.
   - If out of Wi-Fi range (deep in godown): saved to local offline SQLite queue and auto-uploaded as soon as tablet returns in range.

### 4.3 End of Day / Diagnostics
- Check pending orders on PC: `http://localhost:8080/api/orders/pending`.
- In Phase 3, the counter operator triggers the batch invoice import into `FAVWIN`.
