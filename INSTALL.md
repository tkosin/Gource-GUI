# Gource GUI - Installation Guide

This guide provides step-by-step instructions for installing Gource GUI on different operating systems.

## 🚀 Quick Start (Automated Installation)

### Windows
```batch
# Double-click install.bat or run in Command Prompt:
install.bat
```

### macOS / Linux
```bash
# Run in Terminal:
./install.sh
# or
bash install.sh
```

### Manual Python Installation
```bash
# Works on all platforms:
python3 install.py
```

## 📋 System Requirements

### Minimum Requirements
- **Python 3.7+** with tkinter support
- **Git** (for repository analysis)
- **Gource** (for visualization)

### Recommended
- **FFmpeg** (for video export functionality)
- **8GB RAM** (for large repositories)
- **Modern GPU** (for smooth Gource visualization)

## 🛠️ Manual Installation

If the automated installer doesn't work, follow these manual steps:

### 1. Install Python Dependencies

```bash
# Install Python packages
pip install -r requirements.txt
```

### 2. Install System Dependencies

#### macOS (using Homebrew)
```bash
# Required
brew install git gource

# Optional (for video export)
brew install ffmpeg

# If tkinter is missing
brew install python-tk
```

#### Ubuntu/Debian
```bash
# Required
sudo apt-get update
sudo apt-get install git gource python3-tk

# Optional (for video export)
sudo apt-get install ffmpeg
```

#### RHEL/CentOS/Fedora
```bash
# Required
sudo yum install git gource tkinter
# or for newer versions:
sudo dnf install git gource python3-tkinter

# Optional (for video export)
sudo yum install ffmpeg
# or
sudo dnf install ffmpeg
```

#### Arch Linux
```bash
# Required
sudo pacman -S git gource tk

# Optional (for video export)
sudo pacman -S ffmpeg
```

#### Windows
1. **Python**: Download from [python.org](https://python.org) - ⚠️ **Check "Add Python to PATH"**
2. **Git**: Download from [git-scm.com](https://git-scm.com)
3. **Gource**: Download from [gource.io](https://gource.io) or use Chocolatey:
   ```cmd
   choco install gource
   ```
4. **FFmpeg** (optional): Download from [ffmpeg.org](https://ffmpeg.org) or use Chocolatey:
   ```cmd
   choco install ffmpeg
   ```

## 🧪 Testing Installation

### Quick Test
```bash
# Test if application starts
python3 main.py
```

### Dependency Check
```bash
# Check all dependencies
python3 install.py
```

## 🚨 Troubleshooting

### Common Issues

#### "tkinter not found" Error
- **Linux**: `sudo apt-get install python3-tk`
- **macOS**: `brew install python-tk`
- **Windows**: Reinstall Python with tkinter option checked

#### "Gource not found" Error
- **macOS**: `brew install gource`
- **Linux**: `sudo apt-get install gource`
- **Windows**: Download from [gource.io](https://gource.io)

#### "FFmpeg not found" (Video export disabled)
- **macOS**: `brew install ffmpeg`
- **Linux**: `sudo apt-get install ffmpeg`
- **Windows**: Download from [ffmpeg.org](https://ffmpeg.org)

#### "Permission denied" on macOS/Linux
```bash
# Make scripts executable
chmod +x install.sh install.py
```

#### Python version too old
```bash
# Check version
python3 --version

# Upgrade on macOS
brew upgrade python3

# Upgrade on Ubuntu
sudo apt-get update
sudo apt-get install python3.9  # or latest version
```

### Application Won't Start
1. **Check dependencies**: Run `python3 install.py`
2. **Check Python version**: Must be 3.7+
3. **Check file permissions**: Ensure `main.py` is readable
4. **Check working directory**: Run from the project folder

### Video Export Issues
1. **Install FFmpeg**: Required for video export
2. **Check disk space**: Video files can be large
3. **Repository size**: Large repos may take time to process

## 🖥️ Desktop Integration

The installer automatically creates desktop shortcuts:

- **Windows**: `Gource GUI.bat` on Desktop
- **macOS**: `Gource GUI.command` on Desktop  
- **Linux**: `gource-gui.desktop` on Desktop

You can also create custom shortcuts pointing to:
```bash
cd /path/to/gource-gui && python3 main.py
```

## 🔧 Development Setup

For developers who want to modify the code:

```bash
# Clone repository
git clone https://github.com/tkosin/Gource-GUI.git
cd Gource-GUI

# Create virtual environment (recommended)
python3 -m venv venv
source venv/bin/activate  # Linux/macOS
# or
venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt

# Run in development mode
python3 main.py
```

## 📦 Distribution

### Creating Executables
You can create standalone executables using PyInstaller:

```bash
# Install PyInstaller
pip install pyinstaller

# Create executable
pyinstaller --onefile --windowed --name "Gource GUI" main.py

# Executable will be in dist/ folder
```

### Packaging for Distribution
```bash
# Create distributable archive
zip -r gource-gui-v1.0.zip . -x "*.git*" "*__pycache__*" "*.pyc" "venv/*"
```

## 🆘 Getting Help

If you encounter issues:

1. **Check this guide**: Common solutions are listed above
2. **Run diagnostics**: `python3 install.py` shows detailed system info
3. **Check logs**: Look for error messages in the terminal
4. **GitHub Issues**: Report bugs at [GitHub Issues](https://github.com/tkosin/Gource-GUI/issues)

## 📝 Version Information

- **Supported Python**: 3.7+
- **Supported Platforms**: Windows 10+, macOS 10.14+, Linux (Ubuntu 18.04+)
- **Dependencies**: Git, Gource (required), FFmpeg (optional)

---

Created by Yod Kosin and [https://www.letsrover.ai](https://www.letsrover.ai)
