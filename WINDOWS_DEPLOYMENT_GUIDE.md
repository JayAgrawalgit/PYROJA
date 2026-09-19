# Windows Deployment & Operator Guide: PYROJA FoxPro Sync Service

**Version:** 1.0.0  
**Target Operating Systems:** Windows 10, Windows 11, Windows Server 2016 / 2019 / 2022 (64-bit)  
**Package Folder:** `PYRO-Sync-Service/`

> [!TIP]
> **Recommended for Store Operators:** For the modern graphical desktop interface with single-click start/stop, live status indicators, FoxPro data path browsing (`D:\FAVWIN\D2627`), and port testing, see the new [WINDOWS_CONTROL_PANEL_GUIDE.md](file:///Users/jayagrawal/Documents/PYROJA/WINDOWS_CONTROL_PANEL_GUIDE.md).

---

## 1. Quick Start for Store Administrators

### Step 1: Copy Deployment Folder
Copy the entire `PYRO-Sync-Service/` folder to the target Windows computer (for example, `C:\PYRO-Sync-Service`).

### Step 2: Configure FoxPro Data Path
1. Open `config.json` inside `PYRO-Sync-Service/` with **Notepad**.
2. Locate the `"foxpro"` section:
   ```json
   "foxpro": {
     "data_path": "C:\\FAVWIN\\D2627",
     "active_fiscal_year": "D2627"
   }
   ```
3. Update `"data_path"` to the actual location where your FoxPro `.DBF` files (`ITEMMST.DBF`, `NAMEMST.DBF`, etc.) reside.
4. Save and close Notepad.

### Step 3: Start the Service
1. Double-click `start_sync_service.bat`.
2. A black terminal window will appear showing:
   - The detected LAN IP address of your Windows computer (e.g., `192.168.1.100`).
   - The local documentation URL: `http://localhost:8080/docs`.
   - The tablet pairing URL: `http://192.168.1.100:8080`.
   - Table verification status (confirming `ITEMMST.DBF` and `NAMEMST.DBF` were found).
3. Keep this window open while the store or sales operations are active.

---

## 2. Windows Firewall Configuration

For Android tablets on your local Wi-Fi network to communicate with the sync service, port 8080 must be allowed through Windows Defender Firewall.

### Automated Firewall Setup (Run as Administrator)
Open Command Prompt (Admin) and run:
```cmd
netsh advfirewall firewall add rule name="PYROJA Sync Service" dir=in action=allow protocol=TCP localport=8080
```

### Manual Firewall Setup via Windows GUI
1. Open **Control Panel** -> **Windows Defender Firewall**.
2. Click **Advanced settings** in the left sidebar.
3. Select **Inbound Rules** -> click **New Rule...** on the right.
4. Rule Type: Select **Port** -> click **Next**.
5. Protocol and Ports: Select **TCP**, enter Specific local ports: **8080** -> click **Next**.
6. Action: Select **Allow the connection** -> click **Next**.
7. Profile: Check **Domain** and **Private** (uncheck Public if desired) -> click **Next**.
8. Name: Enter `PYROJA FoxPro Sync Service` -> click **Finish**.

---

## 3. Pairing Android POS Tablets

1. Ensure the Android tablet is connected to the **same Wi-Fi network** as the Windows computer.
2. Open the PYROJA POS Application on the tablet.
3. In the top bar or settings dialog, enter the Sync Service address:
   ```
   http://<WINDOWS_COMPUTER_IP>:8080
   ```
   *(Example: `http://192.168.1.50:8080`)*
4. Tap **Sync Now**.
   - The catalog badge will update with active product counts.
   - Customer balances and ledger masters will synchronize immediately.

---

## 4. Running as a Windows Background Service (Optional)

If you prefer the Sync Service to start automatically when Windows boots (without a user logging in), you can use the free open-source service manager **NSSM** (Non-Sucking Service Manager):

1. Download NSSM from `https://nssm.cc/download`.
2. Open Command Prompt as Administrator and run:
   ```cmd
   nssm install PYROSyncService "C:\PYRO-Sync-Service\PYRO-Sync-Service.exe"
   nssm set PYROSyncService AppDirectory "C:\PYRO-Sync-Service"
   nssm set PYROSyncService Description "PYROJA Android POS to FoxPro Sync Service"
   nssm start PYROSyncService
   ```
3. To view logs: Check `C:\PYRO-Sync-Service\logs\sync_service.log`.

---

## 5. Troubleshooting & FAQ

| Symptom | Probable Cause | Action |
| :--- | :--- | :--- |
| `ITEMMST.DBF: MISSING` in console | Incorrect `data_path` in `config.json` | Check the path in `config.json`. Ensure backslashes are doubled (`C:\\FAVWIN\\D2627`). |
| Tablet shows "Sync Failed: Network Error" | Windows Firewall blocking port 8080 | Follow Section 2 above to allow port 8080 in Windows Firewall. |
| Tablet shows "Connection Refused" | IP address changed or computer offline | Double check IP address in `start_sync_service.bat` console window. Assign a static IP or DHCP reservation. |
| Port 8080 already in use | Another application is using port 8080 | Edit `config.json` to change `"port": 8085`, update firewall rule, and restart `start_sync_service.bat`. |
