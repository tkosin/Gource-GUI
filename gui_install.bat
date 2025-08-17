@echo off
REM Windows GUI installer launcher for Gource GUI

echo.
echo ================================================================
echo                Gource GUI - Graphical Installer
echo ================================================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is not installed or not in PATH
    echo.
    echo Please install Python 3.7+ from https://python.org
    echo Make sure to check "Add Python to PATH" during installation
    echo.
    echo After installing Python, run this installer again.
    pause
    exit /b 1
)

echo 🐍 Python found, launching GUI installer...
echo.

REM Launch the GUI installer
python gui_installer.py

REM Check if there was an error
if errorlevel 1 (
    echo.
    echo ❌ GUI installer failed to start
    echo.
    echo Trying command-line installer as fallback...
    python install.py
    pause
) else (
    echo.
    echo GUI installer completed.
)

exit /b 0
