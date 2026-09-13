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
