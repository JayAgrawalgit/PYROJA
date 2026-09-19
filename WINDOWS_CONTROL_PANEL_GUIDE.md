# PYROJA Windows Server Control Panel — Operator & Deployment Guide

**Version:** 1.0.0  
**Target Environment:** Windows 10 (64-bit) billing/server PC  
**Active FoxPro Live Data Path:** `D:\FAVWIN\D2627`  
**Default Service Port:** `8080`

---

## 1. Overview & Safety Guarantees

The **PYROJA Desktop Control Panel** provides a friendly, non-technical graphical interface for running the PYROJA Sync Service on the store's Windows 10 PC. It bridges Android POS ordering tablets with the store's FoxPro (FAVWIN) accounting system.

### Critical Safety Guarantees
- **Strictly Read-Only Live Data:** The control panel and sync service treat `D:\FAVWIN\D2627` as live business data. Starting the server, browsing folders, validating tables, checking health, or stopping the server **never writes to, modifies, or locks FoxPro `.DBF` files**.
- **No VFP Automation:** The service does not automate `VFP6.EXE`, does not create invoices, and does not alter store inventory.
- **Zero Terminal Requirement:** Operators start and stop the service with a single click—no command-line prompts or manual JSON file editing required.

---

## 2. Desktop Control Panel Features

```
+--------------------------------------------------------------------------------+
|  PYROJA FoxPro Sync Service                                   [ RUNNING ]     |
|  Local LAN Gateway between Android POS Tablets and FoxPro                      |
+--------------------------------------------------------------------------------+
|  FoxPro Live Data Directory (Strictly Read-Only)                              |
|  [ D:\FAVWIN\D2627                                ] [ Browse... ] [ Test Folder]|
|  OK: Required FoxPro tables found and verified read-only.                     |
+--------------------------------------------------------------------------------+
|  Network & Tablet Pairing                                                      |
|  Service Port: [ 8080 ] [ Check Port ]  [x] Allow Tablet Wi-Fi Access (0.0.0.0)|
|  Tablet Connection Address: [ http://192.168.1.15:8080          ] [ Copy URL ] |
+--------------------------------------------------------------------------------+
|  [ ▶ Start Server ]  [ ⏹ Stop Server ]  [ Check Health ]  [ Save ] [ Reset ]   |
+--------------------------------------------------------------------------------+
|  Real-Time Server & Sync Activity                                              |
|  +--------------------------------------------------------------------------+  |
|  | [INFO] PYROJA Control Panel initialized.                                 |  |
|  | [INFO] FoxPro live tables verified: ITEMMST, NAMEMST, SALETRN found.     |  |
|  | [INFO] Server successfully started on 0.0.0.0:8080                       |  |
|  | 192.168.1.50 - GET /api/sync/products [200] (12.4ms)                     |  |
|  +--------------------------------------------------------------------------+  |
|  Ready. Server is RUNNING on 0.0.0.0:8080. Tablets may connect.                |
+--------------------------------------------------------------------------------+
```

### 1. FoxPro Data Folder (`D:\FAVWIN\D2627`)
- **Default Path:** Pre-configured to `D:\FAVWIN\D2627`.
- **Test Folder:** Performs a strictly read-only check to ensure that the required FoxPro tables exist and are readable:
  - `ITEMMST.DBF` (Product catalog and inventory)
  - `NAMEMST.DBF` (Customer ledger master)
  - `SALETRN.DBF` (Sales transactions)
  - Optional: `COMPMST.DBF`, `AREAMST.DBF`, `TAXMST.DBF`
- **Browse:** Allows the operator to locate the directory if FoxPro is stored on a different drive or directory.

### 2. Network & Tablet Connection
- **Service Port:** Default is `8080`. Click **Check Port** to verify that the port is free before starting.
- **Allow Tablet Wi-Fi Access:** Enabled by default (binds to `0.0.0.0`). When enabled, Android tablets on the store Wi-Fi can sync catalog and order data.
- **Tablet Connection Address:** Automatically detects the local Wi-Fi IP address (e.g., `http://192.168.1.15:8080`).
- **Copy URL:** Copies the exact connection address to the Windows clipboard with one click.

### 3. Server Controls
- **▶ Start Server:** Launches the background sync service worker. The status badge turns green (`RUNNING`).
- **⏹ Stop Server:** Gracefully shuts down active network listeners and background threads.
- **Check Health:** Queries the live health endpoint and displays active table record counts.
- **Save Settings:** Persists configuration to `%APPDATA%\PYROJA\settings.json`.
- **Reset to Defaults:** Restores `D:\FAVWIN\D2627`, port `8080`, and LAN access.

### 4. Real-Time Activity Log
- Displays table verification results, startup diagnostics, incoming tablet requests, and any warnings in real time.

---

## 3. First-Time Operator Walkthrough

### Step 1: Launch the Application
Double-click `PYROJA-Control-Panel.exe` on the Windows desktop.  
*(Or execute `start_control_panel.bat` if using the source release).*

### Step 2: Verify the FoxPro Folder
1. Confirm the folder path displays: `D:\FAVWIN\D2627`.
2. Click **Test Folder**.
3. A green confirmation will appear:  
   *`Folder verified! All required tables are readable: ITEMMST.DBF, NAMEMST.DBF, SALETRN.DBF.`*

### Step 3: Start the Server
1. Click **▶ Start Server**.
2. The status badge will change to yellow (`STARTING`) and then green (`RUNNING`).
3. The activity log will display:  
   *`[INFO] Server successfully started on 0.0.0.0:8080`*

### Step 4: Connect the Android Tablet
1. Click **Copy URL** next to the Tablet Connection Address (for example, `http://192.168.1.15:8080`).
2. On the Android tablet:
   - Ensure the tablet is connected to the same Wi-Fi router as the Windows PC.
   - Open the **PYROJA POS Application**.
   - Tap **Settings** (gear icon) in the top bar.
   - Paste or type the copied URL into the **Sync Service URL** field.
   - Tap **Save** and then tap **Sync Now**.
3. In the Windows Control Panel log console, you will immediately see:  
   *`192.168.1.xx - GET /api/sync/products [200]`*  
   *`192.168.1.xx - GET /api/sync/customers [200]`*

---

## 4. Windows Firewall Setup (Port 8080)

To allow tablets to reach the sync service over local Wi-Fi, Windows Defender Firewall must allow incoming TCP traffic on port 8080.

### Option A: One-Line Command (Run as Administrator)
Open PowerShell or Command Prompt as Administrator and run:
```cmd
netsh advfirewall firewall add rule name="PYROJA Sync Service" dir=in action=allow protocol=TCP localport=8080
```

### Option B: Windows GUI Setup
1. Press `Windows Key + R`, type `firewall.cpl`, and press **Enter**.
2. In the left sidebar, click **Advanced settings**.
3. Click **Inbound Rules** (left), then click **New Rule...** (right).
4. Rule Type: Select **Port** $\to$ Next.
5. Protocol and Ports: Select **TCP**, enter port **8080** $\to$ Next.
6. Action: Select **Allow the connection** $\to$ Next.
7. Profile: Check **Domain** and **Private** $\to$ Next.
8. Name: Enter `PYROJA Sync Service` $\to$ Finish.

---

## 5. Troubleshooting & FAQ

| Symptom / Error | Cause | Resolution |
| :--- | :--- | :--- |
| **Port 8080 is already in use** | Another service or web server is using port 8080. | In the Control Panel, change **Service Port** to `8085` or `8090`, click **Check Port**, then click **Save Settings** and **Start Server**. Update the tablet URL accordingly. |
| **Directory does not exist: D:\FAVWIN\D2627** | FoxPro is installed on a different drive letter or folder. | Click **Browse...**, navigate to your active financial year directory (e.g. `C:\FAVWIN\D2627` or `E:\FAVWIN\D2627`), and click **Test Folder**. |
| **Missing required FoxPro table: SALETRN.DBF** | Selected folder is not the active fiscal year directory. | Ensure the folder selected contains transaction DBFs (`SALETRN.DBF`, `SALEMST.DBF`) and not just the root software directory. |
| **Tablet shows "Connection Refused" or "Network Error"** | 1. Firewall is blocking port 8080.<br>2. Tablet is connected to mobile data or a different Wi-Fi network.<br>3. Server is not started. | 1. Follow Firewall instructions in Section 4.<br>2. Check that the tablet Wi-Fi is on the same local router as the PC.<br>3. Verify Control Panel badge shows `RUNNING`. |
| **"Another instance of PYROJA Control Panel is already open"** | The control panel is already running in the background or minimized. | Look for the PYROJA icon in the Windows taskbar or system tray. Do not launch multiple copies. |
| **Closing the window while running** | Safety prompt prevents accidental tablet disconnection. | A prompt asks for confirmation before shutting down the server. If confirmed, the server shuts down gracefully before the window closes. |

---

## 6. How to Build the Standalone Windows Executable

To compile `PYROJA-Control-Panel.exe` from source on any Windows 10/11 machine:

### Prerequisites
- Python 3.10+ (64-bit) installed from [python.org](https://www.python.org/downloads/). (Check "Add Python to PATH" during installation).

### Build Instructions
1. Open PowerShell or Command Prompt.
2. Clone or copy the PYROJA repository to the PC:
   ```cmd
   cd C:\path\to\PYROJA\sync-service
   ```
3. Install required dependencies and PyInstaller:
   ```cmd
   pip install -r requirements.txt
   pip install pyinstaller
   ```
4. Run the packaging build:
   ```cmd
   pyinstaller --clean pyroja_control_panel.spec
   ```
5. The standalone executable will be produced in:
   ```
   sync-service\dist\PYROJA-Control-Panel.exe
   ```
6. Distribute `PYROJA-Control-Panel.exe` directly to the billing PC. It requires no Python pre-installation on the operator's account.
