#!/usr/bin/env python3
"""
Cross-platform installer for Gource GUI
Handles dependencies, system requirements, and setup across macOS, Linux, and Windows
"""

import os
import sys
import platform
import subprocess
import shutil
from pathlib import Path

class GourceGUIInstaller:
    def __init__(self):
        self.system = platform.system().lower()
        self.python_version = sys.version_info
        self.project_dir = Path(__file__).parent
        
    def print_header(self):
        print("=" * 60)
        print("         Gource GUI - Cross-Platform Installer")
        print("=" * 60)
        print(f"System: {platform.system()} {platform.release()}")
        print(f"Python: {sys.version}")
        print(f"Architecture: {platform.machine()}")
        print("=" * 60)
        
    def check_python_version(self):
        """Check if Python version is compatible"""
        print("\n🐍 Checking Python version...")
        
        if self.python_version < (3, 7):
            print(f"❌ Python 3.7+ required. You have {sys.version}")
            print("   Please upgrade Python and try again.")
            return False
        
        print(f"✅ Python {sys.version.split()[0]} - Compatible")
        return True
    
    def check_tkinter(self):
        """Check if tkinter is available"""
        print("\n🖼️  Checking tkinter availability...")
        
        try:
            import tkinter
            print("✅ tkinter - Available")
            return True
        except ImportError:
            print("❌ tkinter - Not available")
            print("   Installation required:")
            
            if self.system == "linux":
                print("   sudo apt-get install python3-tk  # Ubuntu/Debian")
                print("   sudo yum install tkinter         # RHEL/CentOS")
                print("   sudo pacman -S tk               # Arch Linux")
            elif self.system == "darwin":
                print("   brew install python-tk")
            elif self.system == "windows":
                print("   tkinter should be included with Python installation")
                print("   Try reinstalling Python from python.org")
            
            return False
    
    def install_python_dependencies(self):
        """Install required Python packages"""
        print("\n📦 Installing Python dependencies...")
        
        requirements_file = self.project_dir / "requirements.txt"
        
        if not requirements_file.exists():
            print("❌ requirements.txt not found")
            return False
        
        try:
            cmd = [sys.executable, "-m", "pip", "install", "-r", str(requirements_file)]
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0:
                print("✅ Python dependencies installed successfully")
                return True
            else:
                print(f"❌ Failed to install Python dependencies:")
                print(result.stderr)
                return False
        except Exception as e:
            print(f"❌ Error installing dependencies: {e}")
            return False
    
    def check_gource(self):
        """Check if Gource is installed"""
        print("\n🎥 Checking Gource installation...")
        
        if shutil.which("gource"):
            try:
                result = subprocess.run(["gource", "--help"], capture_output=True, text=True)
                if result.returncode == 0:
                    print("✅ Gource - Installed and working")
                    return True
            except:
                pass
        
        print("❌ Gource - Not found or not working")
        print("   Installation required:")
        
        if self.system == "darwin":
            print("   brew install gource")
        elif self.system == "linux":
            print("   sudo apt-get install gource     # Ubuntu/Debian")
            print("   sudo yum install gource         # RHEL/CentOS")
            print("   sudo pacman -S gource           # Arch Linux")
        elif self.system == "windows":
            print("   Download from: https://gource.io/")
            print("   Or use chocolatey: choco install gource")
        
        return False
    
    def check_ffmpeg(self):
        """Check if FFmpeg is installed (optional)"""
        print("\n🎬 Checking FFmpeg installation (optional for video export)...")
        
        if shutil.which("ffmpeg"):
            try:
                result = subprocess.run(["ffmpeg", "-version"], capture_output=True, text=True)
                if result.returncode == 0:
                    print("✅ FFmpeg - Installed and working")
                    return True
            except:
                pass
        
        print("⚠️  FFmpeg - Not found (video export will be disabled)")
        print("   To enable video export, install FFmpeg:")
        
        if self.system == "darwin":
            print("   brew install ffmpeg")
        elif self.system == "linux":
            print("   sudo apt-get install ffmpeg     # Ubuntu/Debian")
            print("   sudo yum install ffmpeg         # RHEL/CentOS")
            print("   sudo pacman -S ffmpeg           # Arch Linux")
        elif self.system == "windows":
            print("   Download from: https://ffmpeg.org/")
            print("   Or use chocolatey: choco install ffmpeg")
        
        return False
    
    def check_git(self):
        """Check if Git is installed"""
        print("\n📁 Checking Git installation...")
        
        if shutil.which("git"):
            try:
                result = subprocess.run(["git", "--version"], capture_output=True, text=True)
                if result.returncode == 0:
                    print("✅ Git - Installed and working")
                    return True
            except:
                pass
        
        print("❌ Git - Not found")
        print("   Git is required for repository analysis")
        print("   Installation instructions:")
        
        if self.system == "darwin":
            print("   brew install git")
            print("   Or install Xcode Command Line Tools: xcode-select --install")
        elif self.system == "linux":
            print("   sudo apt-get install git        # Ubuntu/Debian")
            print("   sudo yum install git            # RHEL/CentOS")
            print("   sudo pacman -S git              # Arch Linux")
        elif self.system == "windows":
            print("   Download from: https://git-scm.com/")
        
        return False
    
    def create_desktop_shortcut(self):
        """Create desktop shortcut (platform-specific)"""
        print("\n🖥️  Creating desktop shortcut...")
        
        main_py = self.project_dir / "main.py"
        
        try:
            if self.system == "darwin":
                # macOS: Create .command file
                shortcut_path = Path.home() / "Desktop" / "Gource GUI.command"
                shortcut_content = f'''#!/bin/bash
cd "{self.project_dir}"
python3 "{main_py}"
'''
                shortcut_path.write_text(shortcut_content)
                os.chmod(shortcut_path, 0o755)
                print(f"✅ Desktop shortcut created: {shortcut_path}")
                
            elif self.system == "linux":
                # Linux: Create .desktop file
                shortcut_path = Path.home() / "Desktop" / "gource-gui.desktop"
                shortcut_content = f'''[Desktop Entry]
Version=1.0
Type=Application
Name=Gource GUI
Comment=GUI for Gource version control visualization
Exec=python3 "{main_py}"
Icon=applications-multimedia
Path={self.project_dir}
Terminal=false
StartupNotify=true
Categories=Development;Graphics;
'''
                shortcut_path.write_text(shortcut_content)
                os.chmod(shortcut_path, 0o755)
                print(f"✅ Desktop shortcut created: {shortcut_path}")
                
            elif self.system == "windows":
                # Windows: Create .bat file
                shortcut_path = Path.home() / "Desktop" / "Gource GUI.bat"
                shortcut_content = f'''@echo off
cd /d "{self.project_dir}"
python "{main_py}"
pause
'''
                shortcut_path.write_text(shortcut_content)
                print(f"✅ Desktop shortcut created: {shortcut_path}")
                
            return True
        except Exception as e:
            print(f"⚠️  Could not create desktop shortcut: {e}")
            return False
    
    def test_installation(self):
        """Test if the application can start"""
        print("\n🧪 Testing installation...")
        
        main_py = self.project_dir / "main.py"
        
        if not main_py.exists():
            print("❌ main.py not found")
            return False
        
        try:
            # Test import only (don't start GUI)
            cmd = [sys.executable, "-c", "import sys; sys.path.insert(0, '.'); from gui.main_window_with_video import GourceGUIApp; print('✅ Application modules load successfully')"]
            result = subprocess.run(cmd, cwd=self.project_dir, capture_output=True, text=True, timeout=10)
            
            if result.returncode == 0:
                print(result.stdout.strip())
                return True
            else:
                print(f"❌ Application test failed: {result.stderr}")
                return False
        except subprocess.TimeoutExpired:
            print("❌ Application test timed out")
            return False
        except Exception as e:
            print(f"❌ Application test error: {e}")
            return False
    
    def print_usage_instructions(self):
        """Print instructions on how to use the application"""
        print("\n" + "=" * 60)
        print("                    INSTALLATION COMPLETE!")
        print("=" * 60)
        print("\n🚀 How to run Gource GUI:")
        print("\n1. Command Line:")
        print(f"   cd '{self.project_dir}'")
        print("   python3 main.py")
        
        print("\n2. Desktop Shortcut:")
        if self.system == "darwin":
            print("   Double-click 'Gource GUI.command' on your Desktop")
        elif self.system == "linux":
            print("   Double-click 'gource-gui.desktop' on your Desktop")
        elif self.system == "windows":
            print("   Double-click 'Gource GUI.bat' on your Desktop")
        
        print("\n📖 Usage:")
        print("   1. Click 'Browse...' to select a Git repository")
        print("   2. Configure settings in the 'Basic Settings' tab")
        print("   3. Optionally configure video export in 'Video Export' tab")
        print("   4. Click 'Run Gource' to start visualization")
        print("   5. Click 'Export Video' to render to file")
        
        print("\n💡 Tips:")
        print("   • Make sure your Git repository has commit history")
        print("   • FFmpeg is required for video export functionality")
        print("   • Use 'Preview Command' to see generated Gource command")
        
        print("\n🆘 Support:")
        print("   GitHub: https://github.com/tkosin/Gource-GUI")
        print("   Created by Yod Kosin and https://www.letsrover.ai")
        print("=" * 60)
    
    def install(self):
        """Run the complete installation process"""
        self.print_header()
        
        success = True
        
        # Required checks
        if not self.check_python_version():
            success = False
        
        if not self.check_tkinter():
            success = False
        
        if not self.check_git():
            success = False
        
        if not self.check_gource():
            success = False
        
        # Optional check
        self.check_ffmpeg()
        
        if not success:
            print("\n❌ Installation cannot continue due to missing requirements.")
            print("   Please install the required dependencies and run this script again.")
            return False
        
        # Install Python dependencies
        if not self.install_python_dependencies():
            print("\n❌ Failed to install Python dependencies.")
            return False
        
        # Test installation
        if not self.test_installation():
            print("\n❌ Installation test failed.")
            return False
        
        # Create desktop shortcut
        self.create_desktop_shortcut()
        
        # Show usage instructions
        self.print_usage_instructions()
        
        return True

def main():
    """Main installer function"""
    installer = GourceGUIInstaller()
    
    try:
        success = installer.install()
        if success:
            sys.exit(0)
        else:
            sys.exit(1)
    except KeyboardInterrupt:
        print("\n\n⚠️  Installation cancelled by user.")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Installation failed with error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
