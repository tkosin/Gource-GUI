# Gource GUI

A user-friendly graphical interface for [Gource](https://gource.io), the software version control visualization tool.

![Gource GUI Screenshot](screenshot.png)

## Features

- **Easy Repository Selection**: Browse and select Git repositories with a simple file dialog
- **Visual Settings Panel**: Configure Gource visualization options through an intuitive interface
- **Repository Analysis**: View repository information including commit count, contributors, and programming languages
- **Command Preview**: See the generated Gource command before running
- **Video Export**: Export visualizations directly to MP4/MOV video files
- **Recent Repositories**: Quick access to recently opened repositories
- **Cross-Platform**: Works on macOS, Linux, and Windows

## Prerequisites

1. **Gource** must be installed and accessible in your PATH
   - **macOS**: `brew install gource`
   - **Linux**: `sudo apt-get install gource` (Ubuntu/Debian) or equivalent
   - **Windows**: Download from [gource.io](https://gource.io)

2. **Python 3.7+** with tkinter support (usually included)

3. **FFmpeg** (optional, for video export)
   - **macOS**: `brew install ffmpeg`
   - **Linux**: `sudo apt-get install ffmpeg`
   - **Windows**: Download from [ffmpeg.org](https://ffmpeg.org)

## Installation

### 🚀 Quick Start (Automated)

1. **Clone the repository:**
   ```bash
   git clone https://github.com/tkosin/Gource-GUI.git
   cd Gource-GUI
   ```

2. **Run the installer:**
   
   **Windows:**
   ```batch
   install.bat
   ```
   
   **macOS/Linux:**
   ```bash
   ./install.sh
   ```
   
   **Manual (all platforms):**
   ```bash
   python3 install.py
   ```

The installer will automatically:
- Check system requirements
- Install Python dependencies
- Verify Gource and FFmpeg installation
- Create desktop shortcuts
- Test the installation

### 📋 Requirements
- **Python 3.7+** with tkinter
- **Git** and **Gource** (required)
- **FFmpeg** (optional, for video export)

See [INSTALL.md](INSTALL.md) for detailed installation instructions and troubleshooting.

## Usage

### Option 1: Run with the startup script
```bash
./run_gui.sh
```

### Option 2: Run with Python directly
```bash
source venv/bin/activate  # Activate virtual environment
python3 main.py
```

### Using the GUI

1. **Select Repository**: Click "Browse..." to select a Git repository folder
2. **Configure Settings**: 
   - Choose resolution (640x480, 1280x720, 1920x1080)
   - Set visualization speed (seconds per day)
   - Toggle fullscreen mode
3. **Run Visualization**: Click "Run Gource" to start the visualization

## GUI Components

### Repository Selection
- **Path Entry**: Shows the selected repository path
- **Browse Button**: Opens a folder selection dialog
- **Status Indicator**: Shows validation status (✓ for valid, ✗ for invalid)

### Settings Panel
- **Resolution**: Choose from preset resolutions or custom dimensions
- **Seconds per Day**: Control visualization speed (0.1 - 60 seconds)
- **Display Options**: Hide/show various elements (filenames, usernames, etc.)
- **Visual Settings**: Background color, font scale, camera mode
- **Date Range**: Start/stop dates for visualization

### Action Buttons
- **Preview Command**: View the generated Gource command
- **Run Gource**: Start the visualization
- **Export Video**: Export to MP4/MOV format
- **Stop**: Terminate running visualization

## Supported Repository Types

- **Git** (primary support)
- **SVN** (Subversion)
- **Mercurial**
- **Bazaar**
- **CVS**

## Configuration

Settings are automatically saved to `~/.gource-gui/config.json` and include:
- Window size and position
- Recent repositories list
- Gource settings preferences
- Last export directory

## Troubleshooting

### "Gource not found" Error
- Install Gource using your system's package manager
- Ensure Gource is in your PATH: `which gource`
- On macOS: `brew install gource`

### "Repository validation failed"
- Ensure the selected folder contains a valid Git repository
- Check that the `.git` folder exists in the repository root
- Try running `git status` in the repository folder

### Video Export Issues
- Install FFmpeg: `brew install ffmpeg` (macOS)
- Check FFmpeg installation: `ffmpeg -version`
- Ensure sufficient disk space for video output

### GUI Won't Start
- Install tkinter: `python3-tk` (Linux)
- Check Python version: `python3 --version`
- Install missing dependencies: `pip install -r requirements.txt`

## Development

The project structure:
```
gource-gui/
├── main.py                 # Application entry point
├── requirements.txt        # Python dependencies
├── run_gui.sh             # Startup script
├── gui/                   # GUI components
│   └── main_window_clean.py
├── core/                  # Core functionality
│   ├── gource_runner.py   # Gource command execution
│   └── repository_validator.py # Repository analysis
└── utils/                 # Utilities
    └── config.py          # Configuration management
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License. See LICENSE file for details.

## Credits

- **Gource**: Created by Andrew Caudwell
- **GUI**: Built with Python and Tkinter
- **Icons**: Material Design icons (where applicable)

## Links

- [Gource Official Website](https://gource.io)
- [Gource GitHub Repository](https://github.com/acaudwell/Gource)
- [Python Tkinter Documentation](https://docs.python.org/3/library/tkinter.html)
