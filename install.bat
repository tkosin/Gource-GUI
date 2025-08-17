@echo off
REM Windows installer for Gource GUI
REM This script runs the Python installer with Windows-specific handling

echo.
echo ===============================================================
echo                  Gource GUI - Windows Installer
echo ===============================================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is not installed or not in PATH
    echo.
    echo Please install Python 3.7+ from https://python.org
    echo Make sure to check "Add Python to PATH" during installation
    echo.
    pause
    exit /b 1
)

echo 🐍 Python found, running installer...
echo.

REM Run the Python installer
python install.py

REM Check if installation was successful
if errorlevel 1 (
    echo.
    echo ❌ Installation failed
    pause
    exit /b 1
) else (
    echo.
    echo ✅ Installation completed successfully!
    echo.
)

pause
