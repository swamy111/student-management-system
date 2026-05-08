@echo off
REM Hospital Management System - Desktop Launcher for Windows

echo ========================================
echo   HOSPITAL MANAGEMENT SYSTEM
echo   Starting Application...
echo ========================================
echo.

REM Check if Python is installed
where python >nul 2>nul
if %errorlevel% neq 0 (
    echo ERROR: Python is not installed or not in PATH!
    pause
    exit /b 1
)

REM Navigate to script directory
cd /d "%~dp0"

REM Install Flask if not already installed
echo Installing dependencies...
pip install flask --quiet

echo.
echo Starting Hospital Management System...
echo Opening in your default browser...
echo.

REM Open browser after 2 seconds
timeout /t 2 /nobreak >nul
start http://127.0.0.1:5002

REM Run the application
python app.py

pause
