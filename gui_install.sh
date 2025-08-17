#!/bin/bash
# Cross-platform GUI installer launcher for Gource GUI (macOS/Linux)

set -e  # Exit on any error

echo ""
echo "================================================================"
echo "              Gource GUI - Graphical Installer"
echo "================================================================"
echo ""

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed"
    echo ""
    echo "Installation instructions:"
    if [[ "$OSTYPE" == "darwin"* ]]; then
        echo "  macOS: brew install python3"
        echo "  Or download from: https://python.org"
    elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
        echo "  Ubuntu/Debian: sudo apt-get install python3 python3-pip python3-tk"
        echo "  RHEL/CentOS:   sudo yum install python3 python3-pip python3-tkinter"
        echo "  Arch Linux:    sudo pacman -S python python-pip tk"
    fi
    echo ""
    echo "After installing Python, run this installer again."
    exit 1
fi

# Check Python version
PYTHON_VERSION=$(python3 -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')")
REQUIRED_VERSION="3.7"

if [ "$(printf '%s\n' "$REQUIRED_VERSION" "$PYTHON_VERSION" | sort -V | head -n1)" != "$REQUIRED_VERSION" ]; then
    echo "❌ Python 3.7+ required. You have Python $PYTHON_VERSION"
    echo ""
    echo "Please upgrade Python and try again."
    exit 1
fi

echo "🐍 Python $PYTHON_VERSION found, launching GUI installer..."
echo ""

# Make gui_installer.py executable
chmod +x gui_installer.py

# Check if tkinter is available
echo "🔍 Checking tkinter availability..."
if python3 -c "import tkinter" 2>/dev/null; then
    echo "✅ tkinter is available"
    
    # Launch the GUI installer
    python3 gui_installer.py
    
    if [ $? -eq 0 ]; then
        echo ""
        echo "GUI installer completed successfully!"
    else
        echo ""
        echo "❌ GUI installer failed"
        echo ""
        echo "Trying command-line installer as fallback..."
        python3 install.py
    fi
else
    echo "⚠️  tkinter is not available"
    echo ""
    echo "GUI installer cannot run without tkinter."
    echo "Installing tkinter:"
    
    if [[ "$OSTYPE" == "darwin"* ]]; then
        echo "  macOS: brew install python-tk"
    elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
        echo "  Ubuntu/Debian: sudo apt-get install python3-tk"
        echo "  RHEL/CentOS:   sudo yum install python3-tkinter"
        echo "  Arch Linux:    sudo pacman -S tk"
    fi
    
    echo ""
    echo "Falling back to command-line installer..."
    python3 install.py
fi
