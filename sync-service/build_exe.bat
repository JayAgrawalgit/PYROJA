@echo off
setlocal enabledelayedexpansion
title PYROJA Standalone Windows Executable Builder

cd /d "%~dp0"

echo ================================================================
echo           PYROJA FoxPro Sync Service - EXE Builder
echo ================================================================
echo.

python --version >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo [ERROR] Python was not found in your system PATH!
    echo Please install Python 3.10 or higher from https://www.python.org/
    echo (Make sure to check "Add Python to PATH" during installation)
    pause
    exit /b 1
)

echo [1/3] Verifying Python dependencies...
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python -m pip install pyinstaller

echo.
echo [2/3] Building PYROJA-Control-Panel.exe using PyInstaller...
python -m PyInstaller --clean pyroja_control_panel.spec

if %ERRORLEVEL% neq 0 (
    echo.
    echo [ERROR] PyInstaller build failed! Please check the output above.
    pause
    exit /b 1
)

echo.
echo [3/3] Build Succeeded!
echo Executable generated at:
echo   %~dp0dist\PYROJA-Control-Panel.exe
echo.
echo ================================================================
pause
