#!/bin/bash
# Double-clickable launcher for Gource GUI
# This script can be double-clicked or run from terminal

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Change to the project directory
cd "$SCRIPT_DIR"

echo "================================================================"
echo "                    Gource GUI Launcher"
echo "================================================================"
echo ""
echo "Starting Gource GUI application..."
echo ""

# Check if Python 3 is available
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed or not in PATH"
    echo "Please install Python 3.7+ and try again."
    exit 1
fi

echo "✅ Python found"

# Check if main.py exists
if [ ! -f "main.py" ]; then
    echo "❌ main.py not found"
    echo "Please ensure this script is in the Gource GUI directory."
    exit 1
fi

echo "✅ Application files found"

# Activate virtual environment if it exists
if [ -d "venv" ] && [ -f "venv/bin/activate" ]; then
    source venv/bin/activate
    echo "✅ Virtual environment activated"
fi

# Check if dependencies are installed
echo "🔍 Checking dependencies..."
python3 -c "import sys; sys.path.insert(0, '.'); from gui.main_window_with_video import GourceGUIApp" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "⚠️  Dependencies not installed or missing."
    echo ""
    echo "Please run the installer first:"
    echo "  ./gui_install.sh (GUI installer)"
    echo "  ./install.sh (command-line installer)"
    echo ""
    exit 1
fi

echo "✅ Dependencies verified"
echo ""
echo "🚀 Launching Gource GUI..."
echo ""

# Run the GUI
python3 main.py
