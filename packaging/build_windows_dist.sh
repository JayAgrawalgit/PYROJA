#!/usr/bin/env bash
set -e

DIST_DIR="/workspace/dist/PYRO-Sync-Service"
rm -rf "$DIST_DIR"
mkdir -p "$DIST_DIR"
mkdir -p "$DIST_DIR/site-packages"
mkdir -p "$DIST_DIR/logs"

echo "=== 1. Downloading Windows 64-bit Python 3.11.9 Embeddable Runtime ==="
cd /tmp
curl -sSL https://www.python.org/ftp/python/3.11.9/python-3.11.9-embed-amd64.zip -o py_embed.zip
unzip -q -o py_embed.zip -d "$DIST_DIR"
rm py_embed.zip

# Configure python311._pth
echo "=== 2. Configuring Python sys.path ==="
cat << 'PTH_EOF' > "$DIST_DIR/python311._pth"
python311.zip
.
site-packages
import site
PTH_EOF

echo "=== 3. Downloading and Extracting Windows x86_64 Wheels ==="
WHEELS_TMP="/tmp/wheels"
rm -rf "$WHEELS_TMP"
mkdir -p "$WHEELS_TMP"

pip download \
    --only-binary=:all: \
    --platform win_amd64 \
    --python-version 311 \
    --implementation cp \
    --abi cp311 \
    -d "$WHEELS_TMP" \
    fastapi==0.141.1 \
    uvicorn==0.52.4 \
    pydantic==2.13.5 \
    pydantic-settings==2.15.0 \
    pyyaml==6.0.3 \
    websockets==17.1 \
    httpx==0.28.1 \
    starlette==1.6.0 \
    click \
    h11 \
    idna \
    anyio \
    sniffio \
    typing-extensions

# Extract all downloaded wheels into site-packages
for whl in "$WHEELS_TMP"/*.whl; do
    echo "Extracting $(basename "$whl")..."
    unzip -q -o "$whl" -d "$DIST_DIR/site-packages"
done
rm -rf "$WHEELS_TMP"

echo "=== 4. Compiling Native Windows 64-bit Launcher (PYRO-Sync-Service.exe) ==="
cat << 'C_EOF' > /tmp/launcher.c
#include <windows.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int main(int argc, char *argv[]) {
    char exePath[MAX_PATH];
    DWORD len = GetModuleFileNameA(NULL, exePath, MAX_PATH);
    if (len == 0 || len == MAX_PATH) {
        fprintf(stderr, "Error: Could not determine executable directory.\n");
        return 1;
    }

    char *lastSlash = strrchr(exePath, '\\');
    if (lastSlash != NULL) {
        *lastSlash = '\0';
    }

    SetCurrentDirectoryA(exePath);
    SetConsoleTitleA("PYROJA FoxPro Sync Service");

    char pythonExe[MAX_PATH];
    snprintf(pythonExe, sizeof(pythonExe), "%s\\python.exe", exePath);

    DWORD attrib = GetFileAttributesA(pythonExe);
    if (attrib == INVALID_FILE_ATTRIBUTES || (attrib & FILE_ATTRIBUTE_DIRECTORY)) {
        fprintf(stderr, "Error: Bundled Python runtime not found at: %s\n", pythonExe);
        return 1;
    }

    char cmdLine[8192];
    int offset = snprintf(cmdLine, sizeof(cmdLine), "\"%s\" -m app.main", pythonExe);

    for (int i = 1; i < argc; i++) {
        offset += snprintf(cmdLine + offset, sizeof(cmdLine) - offset, " \"%s\"", argv[i]);
    }

    STARTUPINFOA si;
    PROCESS_INFORMATION pi;
    ZeroMemory(&si, sizeof(si));
    si.cb = sizeof(si);
    si.dwFlags = STARTF_USESTDHANDLES;

    HANDLE hIn = GetStdHandle(STD_INPUT_HANDLE);
    HANDLE hOut = GetStdHandle(STD_OUTPUT_HANDLE);
    HANDLE hErr = GetStdHandle(STD_ERROR_HANDLE);

    SECURITY_ATTRIBUTES sa;
    sa.nLength = sizeof(SECURITY_ATTRIBUTES);
    sa.bInheritHandle = TRUE;
    sa.lpSecurityDescriptor = NULL;

    si.hStdInput = (hIn && hIn != INVALID_HANDLE_VALUE) ? hIn : CreateFileA("NUL", GENERIC_READ, FILE_SHARE_READ, &sa, OPEN_EXISTING, 0, NULL);
    si.hStdOutput = (hOut && hOut != INVALID_HANDLE_VALUE) ? hOut : CreateFileA("NUL", GENERIC_WRITE, FILE_SHARE_WRITE, &sa, OPEN_EXISTING, 0, NULL);
    si.hStdError = (hErr && hErr != INVALID_HANDLE_VALUE) ? hErr : CreateFileA("NUL", GENERIC_WRITE, FILE_SHARE_WRITE, &sa, OPEN_EXISTING, 0, NULL);

    ZeroMemory(&pi, sizeof(pi));

    if (!CreateProcessA(
            NULL,
            cmdLine,
            NULL,
            NULL,
            TRUE,
            0,
            NULL,
            exePath,
            &si,
            &pi
        )) {
        fprintf(stderr, "Failed to launch sync service process (Error %lu).\n", GetLastError());
        return 1;
    }

    WaitForSingleObject(pi.hProcess, INFINITE);
    DWORD exitCode = 0;
    GetExitCodeProcess(pi.hProcess, &exitCode);

    CloseHandle(pi.hProcess);
    CloseHandle(pi.hThread);

    return (int)exitCode;
}
C_EOF

x86_64-w64-mingw32-gcc -O2 -s -mconsole /tmp/launcher.c -o "$DIST_DIR/PYRO-Sync-Service.exe"
rm /tmp/launcher.c

echo "=== 5. Copying Application Code ==="
cp -r /workspace/sync-service/app "$DIST_DIR/app"

echo "=== 6. Creating Default Configuration (config.json) ==="
cat << 'JSON_EOF' > "$DIST_DIR/config.json"
{
  "server": {
    "host": "0.0.0.0",
    "port": 8080,
    "cors_origins": ["*"]
  },
  "foxpro": {
    "data_path": "../legacy-software-extracted/FAVWIN/D2627",
    "active_fiscal_year": "D2627"
  },
  "database": {
    "path": "sync_service.sqlite3"
  },
  "cache": {
    "ttl_seconds": 30,
    "validate_mtime": true
  },
  "logging": {
    "level": "INFO",
    "format": "%(asctime)s [%(levelname)s] [%(name)s] %(message)s",
    "file": "logs/sync_service.log"
  }
}
JSON_EOF

echo "=== 7. Creating start_sync_service.bat Launcher Script ==="
cat << 'BAT_EOF' > "$DIST_DIR/start_sync_service.bat"
@echo off
setlocal enabledelayedexpansion
title PYROJA FoxPro Sync Service

cd /d "%~dp0"

echo ================================================================
echo           PYROJA FoxPro Windows Sync Service
echo ================================================================
echo.

if not exist "%~dp0PYRO-Sync-Service.exe" (
    echo [ERROR] PYRO-Sync-Service.exe not found in "%~dp0"!
    pause
    exit /b 1
)

:: Auto-detect Local LAN IP address
set "LOCAL_IP=localhost"
for /f "tokens=4" %%a in ('route print ^| findstr 0.0.0.0 ^| findstr /v "0.0.0.0.*0.0.0.0"') do (
    set "LOCAL_IP=%%a"
)

echo [STATUS] Starting Sync Service on 0.0.0.0:8080...
echo [INFO] Local Web URL:     http://localhost:8080/docs
echo [INFO] Tablet LAN URL:    http://!LOCAL_IP!:8080
echo [INFO] Health Endpoint:   http://localhost:8080/api/health
echo [INFO] Log File:          logs\sync_service.log
echo [INFO] Press CTRL+C to stop the server at any time.
echo.
echo ================================================================
echo.

:: Launch the executable
"%~dp0PYRO-Sync-Service.exe"

if %ERRORLEVEL% neq 0 (
    echo.
    echo [WARNING] Sync Service stopped with exit code %ERRORLEVEL%.
    pause
)
BAT_EOF

echo "=== 8. Creating VERSION.txt and README.txt ==="
cat << 'VER_EOF' > "$DIST_DIR/VERSION.txt"
PYROJA FoxPro Sync Service v1.0.0
Build Architecture: Windows x86_64 (64-bit Standalone)
Runtime: Embedded Python 3.11.9
Compatibility: Windows 10, Windows 11, Windows Server 2016/2019/2022
Built Date: 2026-09-13
VER_EOF

cat << 'TXT_EOF' > "$DIST_DIR/README.txt"
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
TXT_EOF

echo "=== Build Complete! Package assembled at $DIST_DIR ==="
ls -la "$DIST_DIR"
