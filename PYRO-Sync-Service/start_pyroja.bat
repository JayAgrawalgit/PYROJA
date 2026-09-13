@echo off
setlocal enabledelayedexpansion
title PYROJA

cd /d "%~dp0"

echo ================================================================
echo           PYROJA - Retail POS ^& FoxPro Sync System
echo ================================================================
echo.

set "EXE_NAME=PYROJA.exe"
if not exist "%~dp0%EXE_NAME%" (
    if exist "%~dp0PYRO-Sync-Service.exe" (
        set "EXE_NAME=PYRO-Sync-Service.exe"
    ) else if exist "%~dp0PYROJA-Sync-Service.exe" (
        set "EXE_NAME=PYROJA-Sync-Service.exe"
    ) else (
        echo [ERROR] No PYROJA executable found in "%~dp0"!
        pause
        exit /b 1
    )
)

:: Auto-detect Local LAN IP address
set "LOCAL_IP=localhost"
for /f "tokens=4" %%a in ('route print ^| findstr 0.0.0.0 ^| findstr /v "0.0.0.0.*0.0.0.0"') do (
    set "LOCAL_IP=%%a"
)

echo [STATUS] Starting PYROJA on 0.0.0.0:8080...
echo [INFO] Local Web URL:     http://localhost:8080/docs
echo [INFO] Tablet LAN URL:    http://!LOCAL_IP!:8080
echo [INFO] Health Endpoint:   http://localhost:8080/api/health
echo [INFO] Log File:          logs\sync_service.log
echo [INFO] Press CTRL+C to stop the server at any time.
echo.
echo ================================================================
echo.

"%~dp0!EXE_NAME!"

if %ERRORLEVEL% neq 0 (
    echo.
    echo [WARNING] PYROJA stopped with exit code %ERRORLEVEL%.
    pause
)
