#!/bin/bash
# Double-clickable launcher for Gource GUI on Linux
# This script can be double-clicked from the desktop or file manager to launch the application

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Change to the project directory
cd "$SCRIPT_DIR"

# Function to display error and wait for user input
show_error() {
    echo ""
    echo "❌ $1"
    echo ""
    echo "Press Enter to continue..."
    read
}

# Function to display success message
show_success() {
    echo "✅ $1"
}

# Function to check if running in terminal
is_terminal() {
    [ -t 1 ]
}

# If not running in terminal, try to open in terminal
if ! is_terminal; then
    # Try different terminal emulators
    if command -v gnome-terminal &> /dev/null; then
        gnome-terminal -- bash "$0"
        exit 0
    elif command -v xterm &> /dev/null; then
        xterm -e bash "$0"
        exit 0
    elif command -v konsole &> /dev/null; then
        konsole -e bash "$0"
        exit 0
    elif command -v xfce4-terminal &> /dev/null; then
        xfce4-terminal -e "bash $0"
        exit 0
    else
        # Fallback: create a temporary desktop notification
        if command -v notify-send &> /dev/null; then
            notify-send "Gource GUI" "Please run this script from a terminal: $0"
        fi
        exit 1
    fi
fi

# Clear the terminal for a clean start
clear

echo "================================================================"
echo "                    Gource GUI Launcher"
echo "================================================================"
echo ""
echo "Starting Gource GUI application..."
echo ""

# Check if Python 3 is available
if ! command -v python3 &> /dev/null; then
    show_error "Python 3 is not installed or not in PATH. Please install Python 3.7+ and try again."
    exit 1
fi

# Check Python version
PYTHON_VERSION=$(python3 -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')")
REQUIRED_VERSION="3.7"

if [ "$(printf '%s\n' "$REQUIRED_VERSION" "$PYTHON_VERSION" | sort -V | head -n1)" != "$REQUIRED_VERSION" ]; then
    show_error "Python 3.7+ required. You have Python $PYTHON_VERSION. Please upgrade Python and try again."
    exit 1
fi

show_success "Python $PYTHON_VERSION found"

# Check if main.py exists
if [ ! -f "main.py" ]; then
    show_error "main.py not found. Please ensure this script is in the Gource GUI directory."
    exit 1
fi

show_success "Application files found"

# Check if dependencies are installed
echo "🔍 Checking dependencies..."
python3 -c "import sys; sys.path.insert(0, '.'); from gui.main_window_with_video import GourceGUIApp" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "⚠️  Dependencies not installed or missing."
    echo ""
    echo "Would you like to run the installer first? (y/n)"
    read -r REPLY
    
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        echo ""
        echo "🚀 Running installer..."
        
        # Try GUI installer first, then fallback to command-line
        if command -v python3 &> /dev/null && python3 -c "import tkinter" 2>/dev/null; then
            echo "Launching GUI installer..."
            python3 gui_installer.py
        else
            echo "GUI not available, using command-line installer..."
            python3 install.py
        fi
        
        if [ $? -eq 0 ]; then
            echo ""
            echo "✅ Installation completed! Launching Gource GUI..."
            echo ""
        else
            show_error "Installation failed. Please check the error messages above."
            exit 1
        fi
    else
        echo ""
        echo "Please run the installer first:"
        echo "  ./gui_install.sh (GUI installer)"
        echo "  ./install.sh (command-line installer)"
        echo ""
        echo "Press Enter to exit..."
        read
        exit 1
    fi
fi

show_success "Dependencies verified"

# Launch the application
echo ""
echo "🚀 Launching Gource GUI..."
echo ""
echo "Note: You can close this terminal window after the GUI opens."
echo ""

# Launch the GUI application in background to allow terminal to be closed
python3 main.py &
GUI_PID=$!

# Wait a moment to see if the GUI starts successfully
sleep 2

# Check if the process is still running (GUI started successfully)
if kill -0 $GUI_PID 2>/dev/null; then
    echo "✅ Gource GUI started successfully!"
    echo ""
    echo "You can now close this terminal window."
    echo "Press Enter to close this launcher..."
    read
else
    echo ""
    show_error "Failed to launch Gource GUI. Please check for error messages."
fi

exit 0
