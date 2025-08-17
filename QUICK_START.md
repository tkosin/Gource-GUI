# Gource GUI - Quick Start Guide

## 🚀 Easiest Way to Run Gource GUI (Double-Click Launchers)

After installing Gource GUI, you can easily launch it by double-clicking the appropriate launcher for your operating system:

### 🍎 **macOS**
Double-click: **`Gource GUI.command`**
- This will open Terminal and launch the application
- You can close the Terminal window after the GUI opens

### 🪟 **Windows** 
Double-click: **`Gource GUI.bat`**
- This will open Command Prompt and launch the application
- You can close the Command Prompt after the GUI opens

### 🐧 **Linux**
Double-click: **`Gource GUI.sh`** or **`Gource GUI.desktop`**
- The .sh file will open Terminal and launch the application
- The .desktop file works like a standard Linux application shortcut

### 🔧 **Alternative (All Platforms)**
Double-click: **`run_gui.sh`** (requires bash)
- Universal launcher that works on macOS, Linux, and Windows with bash

---

## 📋 What the Launchers Do

The double-click launchers automatically:

1. ✅ **Check Python Installation** - Verify Python 3.7+ is available
2. ✅ **Validate Application Files** - Ensure all required files are present  
3. ✅ **Check Dependencies** - Verify all Python packages are installed
4. 🛠️ **Offer Installation** - Prompt to run installer if dependencies are missing
5. 🚀 **Launch Application** - Start the Gource GUI interface

---

## 🆘 If Double-Click Doesn't Work

### macOS Issues:
- **"Permission denied"**: Right-click → "Open With" → Terminal
- **"Unidentified developer"**: System Preferences → Security & Privacy → Allow
- **Python not found**: Install Python 3.7+ from python.org or use Homebrew

### Windows Issues:
- **"Python not found"**: Install Python from python.org and check "Add to PATH"
- **Script won't run**: Right-click → "Run as administrator"
- **Command Prompt closes**: Dependencies might be missing - run installer

### Linux Issues:
- **Not executable**: Run `chmod +x "Gource GUI.sh"` in terminal
- **No terminal opens**: Try right-click → "Open in Terminal"
- **Python not found**: Install python3 using your package manager

---

## 🛠️ Manual Installation (If Needed)

If the launchers indicate missing dependencies, install them first:

### GUI Installer (Recommended):
```bash
# Windows
gui_install.bat

# macOS/Linux  
./gui_install.sh
```

### Command-line Installer:
```bash
# Windows
install.bat

# macOS/Linux
./install.sh
```

---

## 🎯 Using Gource GUI

Once launched:

1. **Select Repository**: Click "Browse..." to choose a Git repository folder
2. **Configure Settings**: Adjust resolution, speed, and visual options  
3. **Preview Command**: Use "Preview Command" to see the Gource command
4. **Run Visualization**: Click "Run Gource" to start the visualization
5. **Export Video**: Use "Export Video" to save as MP4/AVI/MOV

---

## 🔗 Need Help?

- **Detailed Installation**: See [INSTALL.md](INSTALL.md)
- **Full Documentation**: See [README.md](README.md)
- **Issues/Bugs**: Visit [GitHub Issues](https://github.com/tkosin/Gource-GUI/issues)

---

## 💡 Pro Tips

- **First-time use**: Run the GUI installer once to set everything up
- **Multiple repositories**: The GUI remembers recent repositories
- **Large repositories**: May take time to process - be patient
- **Video export**: Requires FFmpeg (installer will check and guide you)
- **Desktop shortcuts**: Installers create shortcuts automatically

---

**Created by Yod Kosin and [https://www.letsrover.ai](https://www.letsrover.ai)**
