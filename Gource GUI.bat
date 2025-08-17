@echo off
REM Double-clickable launcher for Gource GUI on Windows
REM This script can be double-clicked from Explorer to launch the application

title Gource GUI Launcher

REM Change to the directory where this batch file is located
cd /d "%~dp0"

echo.
echo ================================================================
echo                    Gource GUI Launcher
echo ================================================================
echo.
echo Starting Gource GUI application...
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is not installed or not in PATH
    echo.
    echo Please install Python 3.7+ from https://python.org
    echo Make sure to check "Add Python to PATH" during installation
    echo.
    echo After installing Python, run this launcher again.
    echo.
    pause
    exit /b 1
)

REM Get Python version (simple check)
for /f "tokens=2" %%i in ('python --version 2^>nul') do set PYTHON_VERSION=%%i
echo ✅ Python %PYTHON_VERSION% found

REM Check if main.py exists
if not exist "main.py" (
    echo.
    echo ❌ main.py not found
    echo Please ensure this script is in the Gource GUI directory.
    echo.
    pause
    exit /b 1
)

echo ✅ Application files found

REM Check if dependencies are installed
echo 🔍 Checking dependencies...
python -c "import sys; sys.path.insert(0, '.'); from gui.main_window_with_video import GourceGUIApp" >nul 2>&1
if errorlevel 1 (
    echo ⚠️  Dependencies not installed or missing.
    echo.
    set /p INSTALL_CHOICE="Would you like to run the installer first? (y/n): "
    
    if /i "%INSTALL_CHOICE%"=="y" (
        echo.
        echo 🚀 Running installer...
        
        REM Try GUI installer first, then fallback to command-line
        python -c "import tkinter" >nul 2>&1
        if not errorlevel 1 (
            echo Launching GUI installer...
            python gui_installer.py
        ) else (
            echo GUI not available, using command-line installer...
            python install.py
        )
        
        if not errorlevel 1 (
            echo.
            echo ✅ Installation completed! Launching Gource GUI...
            echo.
        ) else (
            echo.
            echo ❌ Installation failed. Please check the error messages above.
            echo.
            pause
            exit /b 1
        )
    ) else (
        echo.
        echo Please run the installer first:
        echo   gui_install.bat (GUI installer)
        echo   install.bat (command-line installer)
        echo.
        pause
        exit /b 1
    )
)

echo ✅ Dependencies verified

REM Launch the application
echo.
echo 🚀 Launching Gource GUI...
echo.
echo Note: You can close this window after the GUI opens.
echo.

REM Launch the GUI application
python main.py

REM Check if the application started successfully
if errorlevel 1 (
    echo.
    echo ❌ Failed to launch Gource GUI. Please check the error messages above.
    echo.
    pause
) else (
    echo.
    echo Gource GUI has been closed.
    echo.
    pause
)

exit /b 0
