#!/bin/bash
# Cross-platform installer for Gource GUI (macOS/Linux)

set -e  # Exit on any error

echo ""
echo "==============================================================="
echo "              Gource GUI - Unix/Linux Installer"
echo "==============================================================="
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
        echo "  Ubuntu/Debian: sudo apt-get install python3 python3-pip"
        echo "  RHEL/CentOS:   sudo yum install python3 python3-pip"
        echo "  Arch Linux:    sudo pacman -S python python-pip"
    fi
    echo ""
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

echo "🐍 Python $PYTHON_VERSION found, running installer..."
echo ""

# Make install.py executable
chmod +x install.py

# Run the Python installer
python3 install.py

# Check if installation was successful
if [ $? -eq 0 ]; then
    echo ""
    echo "✅ Installation completed successfully!"
    echo ""
else
    echo ""
    echo "❌ Installation failed"
    exit 1
fi
