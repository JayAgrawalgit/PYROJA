@echo off
setlocal enabledelayedexpansion
title PYROJA FoxPro Sync Service - Desktop Control Panel

cd /d "%~dp0"

echo ================================================================
echo           PYROJA FoxPro Sync Service - Control Panel
echo ================================================================
echo.

:: Check if Python is installed in PATH
python --version >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo [ERROR] Python was not found in your system PATH!
    echo Please install Python 3.10 or higher or run the standalone EXE.
    pause
    exit /b 1
)

:: Launch desktop control panel
python -m app.desktop

if %ERRORLEVEL% neq 0 (
    echo.
    echo [INFO] Control panel closed with exit code %ERRORLEVEL%.
)
