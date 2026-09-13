================================================================================
                    PYROJA FoxPro Windows Sync Service
                               Version 1.0.0
================================================================================

OVERVIEW:
This service bridges the Android Tablet Ordering Application with the legacy
Visual FoxPro 6.0 system (FAVWIN). It provides local LAN synchronization for:
- Product catalogs and real-time inventory counts
- Customer master lists and ledger account balances
- Instant bill booking and offline order queueing into SQLite WAL mode

SYSTEM REQUIREMENTS:
- Windows 10, Windows 11, or Windows Server 2016+ (64-bit)
- No Python installation required (100% self-contained)
- No FoxPro ODBC driver required (pure binary DBF decoding)
- Port 8080 open on local Windows Firewall for tablet access

HOW TO RUN:
1. Double-click "start_sync_service.bat"
   - A command prompt window will open displaying the detected LAN IP address.
   - The sync service will initialize SQLite tables and verify DBF paths.
2. Verify in your web browser:
   - Health check: http://localhost:8080/api/health
   - Interactive API documentation: http://localhost:8080/docs
3. In the Android Tablet app settings:
   - Set Sync Service URL to: http://<YOUR_WINDOWS_IP>:8080

CONFIGURATION (config.json):
The "config.json" file can be edited in Notepad:
- "server":
    "port": Port number (default 8080)
- "foxpro":
    "data_path": Full or relative path to your FoxPro fiscal directory (e.g. "C:\\FAVWIN\\D2627")
    "active_fiscal_year": Current active financial year code (e.g. "D2627")
- "logging":
    "level": "INFO", "DEBUG", or "WARNING"
    "file": Path to log file (default "logs/sync_service.log")

After editing config.json, restart start_sync_service.bat for changes to take effect.

LOGS & TROUBLESHOOTING:
- Log files are written to the "logs/" folder.
- If tablets cannot connect, ensure port 8080 is permitted in Windows Defender Firewall:
  Control Panel -> Windows Defender Firewall -> Advanced Settings -> Inbound Rules -> New Rule -> Port -> TCP -> 8080 -> Allow the connection.
================================================================================
