@echo off
REM Windows Sync Service - Test Suite Runner
cd /d "%~dp0.."
echo ===================================================
echo Running Test Suite
echo ===================================================

if exist .venv\Scripts\pytest.exe (
    set "PYTEST_EXE=.venv\Scripts\pytest.exe"
) else (
    set "PYTEST_EXE=pytest"
)

"%PYTEST_EXE%" -v
pause
