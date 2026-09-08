@echo off
REM Windows Sync Service - Start Server Script
cd /d "%~dp0.."
echo ===================================================
echo Starting PYROWHOLESALE FoxPro Windows Sync Service
echo ===================================================

if exist .venv\Scripts\python.exe (
    set "PYTHON_EXE=.venv\Scripts\python.exe"
) else (
    set "PYTHON_EXE=python"
)

"%PYTHON_EXE%" -m uvicorn app.main:app --host 0.0.0.0 --port 8080
pause
