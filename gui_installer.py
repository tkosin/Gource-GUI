#!/usr/bin/env python3
"""
Cross-platform GUI installer for Gource GUI
Provides a user-friendly graphical installation experience
"""

import os
import sys
import platform
import subprocess
import shutil
import threading
import time
from pathlib import Path
from typing import Optional, Callable

try:
    import tkinter as tk
    from tkinter import ttk, messagebox, filedialog, scrolledtext
except ImportError:
    print("❌ tkinter is required for the GUI installer")
    print("Please install tkinter and try again, or use the command-line installer:")
    print("  python3 install.py")
    sys.exit(1)

class GourceGUIInstallerWindow:
    def __init__(self):
        self.root = tk.Tk()
        self.system = platform.system().lower()
        self.python_version = sys.version_info
        self.project_dir = Path(__file__).parent
        self.installation_thread = None
        self.installation_cancelled = False
        
        # Installation status tracking
        self.checks = {
            'python': {'status': 'pending', 'required': True},
            'tkinter': {'status': 'pending', 'required': True},
            'git': {'status': 'pending', 'required': True},
            'gource': {'status': 'pending', 'required': True},
            'ffmpeg': {'status': 'pending', 'required': False},
            'python_deps': {'status': 'pending', 'required': True},
        }
        
        self.setup_ui()
        
    def setup_ui(self):
        """Set up the GUI installer interface"""
        self.root.title("Gource GUI - Installer")
        self.root.geometry("800x700")
        self.root.resizable(True, True)
        
        # Center window
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() // 2) - (800 // 2)
        y = (self.root.winfo_screenheight() // 2) - (700 // 2)
        self.root.geometry(f"800x700+{x}+{y}")
        
        self.create_header()
        self.create_system_info()
        self.create_requirements_section()
        self.create_progress_section()
        self.create_log_section()
        self.create_buttons()
        self.create_footer()
        
        # Start initial system check
        self.root.after(1000, self.start_system_check)
        
    def create_header(self):
        """Create header section"""
        header_frame = ttk.Frame(self.root)
        header_frame.pack(fill=tk.X, padx=20, pady=10)
        
        title_label = tk.Label(
            header_frame,
            text="Gource GUI Installer",
            font=('Helvetica', 18, 'bold'),
            fg='#2c3e50'
        )
        title_label.pack()
        
        subtitle_label = tk.Label(
            header_frame,
            text="Cross-platform installation wizard for Gource visualization GUI",
            font=('Helvetica', 10),
            fg='#7f8c8d'
        )
        subtitle_label.pack(pady=(5, 0))
        
    def create_system_info(self):
        """Create system information section"""
        info_frame = ttk.LabelFrame(self.root, text="System Information", padding=10)
        info_frame.pack(fill=tk.X, padx=20, pady=(0, 10))
        
        system_info = f"""
Operating System: {platform.system()} {platform.release()}
Architecture: {platform.machine()}
Python Version: {sys.version.split()[0]}
Installation Path: {self.project_dir}
        """.strip()
        
        info_label = tk.Label(info_frame, text=system_info, font=('Courier', 9), justify=tk.LEFT)
        info_label.pack(anchor=tk.W)
        
    def create_requirements_section(self):
        """Create requirements checking section"""
        req_frame = ttk.LabelFrame(self.root, text="Requirements Check", padding=10)
        req_frame.pack(fill=tk.X, padx=20, pady=(0, 10))
        
        # Create grid for requirement items
        self.req_vars = {}
        self.req_labels = {}
        
        requirements = [
            ('python', 'Python 3.7+', True),
            ('tkinter', 'tkinter (GUI library)', True),
            ('git', 'Git (version control)', True),
            ('gource', 'Gource (visualization tool)', True),
            ('ffmpeg', 'FFmpeg (video export)', False),
            ('python_deps', 'Python dependencies', True),
        ]
        
        for i, (key, desc, required) in enumerate(requirements):
            # Status icon
            status_var = tk.StringVar(value="⏳")
            self.req_vars[key] = status_var
            
            status_label = tk.Label(req_frame, textvariable=status_var, font=('Arial', 12))
            status_label.grid(row=i, column=0, sticky=tk.W, padx=(0, 10))
            
            # Description
            req_text = f"{desc}"
            if not required:
                req_text += " (optional)"
                
            desc_label = tk.Label(req_frame, text=req_text, font=('Arial', 10))
            desc_label.grid(row=i, column=1, sticky=tk.W)
            
            # Status text
            status_text_var = tk.StringVar(value="Checking...")
            status_text_label = tk.Label(req_frame, textvariable=status_text_var, 
                                       font=('Arial', 9), fg='#7f8c8d')
            status_text_label.grid(row=i, column=2, sticky=tk.W, padx=(10, 0))
            
            self.req_labels[key] = {
                'status': status_var,
                'text': status_text_var
            }
            
        # Configure grid weights
        req_frame.columnconfigure(1, weight=1)
        
    def create_progress_section(self):
        """Create installation progress section"""
        progress_frame = ttk.LabelFrame(self.root, text="Installation Progress", padding=10)
        progress_frame.pack(fill=tk.X, padx=20, pady=(0, 10))
        
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(
            progress_frame, 
            variable=self.progress_var,
            maximum=100,
            length=400
        )
        self.progress_bar.pack(fill=tk.X)
        
        self.progress_text = tk.StringVar(value="Ready to install")
        progress_label = tk.Label(progress_frame, textvariable=self.progress_text, 
                                font=('Arial', 9))
        progress_label.pack(pady=(5, 0))
        
    def create_log_section(self):
        """Create installation log section"""
        log_frame = ttk.LabelFrame(self.root, text="Installation Log", padding=10)
        log_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 10))
        
        self.log_text = scrolledtext.ScrolledText(
            log_frame,
            height=10,
            font=('Courier', 8),
            wrap=tk.WORD
        )
        self.log_text.pack(fill=tk.BOTH, expand=True)
        
        # Add initial message
        self.log("Gource GUI Installer started")
        self.log(f"System: {platform.system()} {platform.release()}")
        self.log(f"Python: {sys.version}")
        
    def create_buttons(self):
        """Create action buttons"""
        button_frame = ttk.Frame(self.root)
        button_frame.pack(fill=tk.X, padx=20, pady=(0, 10))
        
        # Left side - Help button
        help_button = ttk.Button(
            button_frame,
            text="Help",
            command=self.show_help
        )
        help_button.pack(side=tk.LEFT)
        
        # Right side buttons
        right_frame = ttk.Frame(button_frame)
        right_frame.pack(side=tk.RIGHT)
        
        self.install_button = ttk.Button(
            right_frame,
            text="Install",
            command=self.start_installation,
            state=tk.DISABLED
        )
        self.install_button.pack(side=tk.RIGHT, padx=(5, 0))
        
        self.cancel_button = ttk.Button(
            right_frame,
            text="Cancel",
            command=self.cancel_installation
        )
        self.cancel_button.pack(side=tk.RIGHT, padx=(5, 0))
        
        # Test installation button (enabled after successful install)
        self.test_button = ttk.Button(
            right_frame,
            text="Test Installation",
            command=self.test_installation,
            state=tk.DISABLED
        )
        self.test_button.pack(side=tk.RIGHT, padx=(5, 0))
        
    def create_footer(self):
        """Create footer with credits"""
        footer_frame = ttk.Frame(self.root)
        footer_frame.pack(fill=tk.X, padx=20, pady=(0, 10))
        
        ttk.Separator(footer_frame, orient='horizontal').pack(fill=tk.X, pady=(0, 5))
        
        credits_label = tk.Label(
            footer_frame,
            text="Created by Yod Kosin and https://www.letsrover.ai",
            font=('Arial', 8),
            fg='#7f8c8d'
        )
        credits_label.pack()
        
    def log(self, message: str, level: str = "INFO"):
        """Add message to installation log"""
        timestamp = time.strftime("%H:%M:%S")
        log_entry = f"[{timestamp}] {level}: {message}\n"
        
        self.log_text.insert(tk.END, log_entry)
        self.log_text.see(tk.END)
        self.root.update_idletasks()
        
    def update_requirement_status(self, key: str, status: str, text: str):
        """Update requirement check status"""
        icons = {
            'pending': '⏳',
            'checking': '🔍',
            'success': '✅',
            'warning': '⚠️',
            'error': '❌'
        }
        
        colors = {
            'pending': '#7f8c8d',
            'checking': '#3498db',
            'success': '#27ae60',
            'warning': '#f39c12',
            'error': '#e74c3c'
        }
        
        if key in self.req_labels:
            self.req_labels[key]['status'].set(icons.get(status, '❓'))
            self.req_labels[key]['text'].set(text)
            
        self.checks[key]['status'] = status
        self.root.update_idletasks()
        
    def start_system_check(self):
        """Start checking system requirements in a separate thread"""
        def check_thread():
            self.check_all_requirements()
            
        thread = threading.Thread(target=check_thread, daemon=True)
        thread.start()
        
    def check_all_requirements(self):
        """Check all system requirements"""
        self.log("Starting system requirements check...")
        
        # Check Python version
        self.update_requirement_status('python', 'checking', 'Checking version...')
        if self.python_version >= (3, 7):
            self.update_requirement_status('python', 'success', f'Version {sys.version.split()[0]}')
            self.log(f"Python version check passed: {sys.version.split()[0]}")
        else:
            self.update_requirement_status('python', 'error', f'Version {sys.version.split()[0]} too old')
            self.log(f"Python version check failed: {sys.version.split()[0]} (need 3.7+)", "ERROR")
            
        # Check tkinter
        self.update_requirement_status('tkinter', 'checking', 'Checking availability...')
        try:
            import tkinter
            self.update_requirement_status('tkinter', 'success', 'Available')
            self.log("tkinter check passed")
        except ImportError:
            self.update_requirement_status('tkinter', 'error', 'Not available')
            self.log("tkinter check failed", "ERROR")
            
        # Check Git
        self.update_requirement_status('git', 'checking', 'Checking installation...')
        if shutil.which('git'):
            try:
                result = subprocess.run(['git', '--version'], capture_output=True, text=True, timeout=5)
                if result.returncode == 0:
                    version = result.stdout.strip()
                    self.update_requirement_status('git', 'success', 'Installed')
                    self.log(f"Git check passed: {version}")
                else:
                    self.update_requirement_status('git', 'error', 'Not working')
                    self.log("Git check failed: command error", "ERROR")
            except (subprocess.TimeoutExpired, Exception) as e:
                self.update_requirement_status('git', 'error', 'Not working')
                self.log(f"Git check failed: {e}", "ERROR")
        else:
            self.update_requirement_status('git', 'error', 'Not installed')
            self.log("Git check failed: not found in PATH", "ERROR")
            
        # Check Gource
        self.update_requirement_status('gource', 'checking', 'Checking installation...')
        if shutil.which('gource'):
            try:
                result = subprocess.run(['gource', '--help'], capture_output=True, text=True, timeout=5)
                if result.returncode == 0:
                    self.update_requirement_status('gource', 'success', 'Installed')
                    self.log("Gource check passed")
                else:
                    self.update_requirement_status('gource', 'error', 'Not working')
                    self.log("Gource check failed: command error", "ERROR")
            except (subprocess.TimeoutExpired, Exception) as e:
                self.update_requirement_status('gource', 'error', 'Not working')
                self.log(f"Gource check failed: {e}", "ERROR")
        else:
            self.update_requirement_status('gource', 'error', 'Not installed')
            self.log("Gource check failed: not found in PATH", "ERROR")
            
        # Check FFmpeg (optional)
        self.update_requirement_status('ffmpeg', 'checking', 'Checking installation...')
        if shutil.which('ffmpeg'):
            try:
                result = subprocess.run(['ffmpeg', '-version'], capture_output=True, text=True, timeout=5)
                if result.returncode == 0:
                    self.update_requirement_status('ffmpeg', 'success', 'Installed')
                    self.log("FFmpeg check passed")
                else:
                    self.update_requirement_status('ffmpeg', 'warning', 'Not working')
                    self.log("FFmpeg check failed: command error", "WARNING")
            except (subprocess.TimeoutExpired, Exception) as e:
                self.update_requirement_status('ffmpeg', 'warning', 'Not working')
                self.log(f"FFmpeg check failed: {e}", "WARNING")
        else:
            self.update_requirement_status('ffmpeg', 'warning', 'Not installed')
            self.log("FFmpeg not found (video export will be disabled)", "WARNING")
            
        # Check if ready to install
        self.root.after(0, self.check_installation_readiness)
        
    def check_installation_readiness(self):
        """Check if all required dependencies are met"""
        ready = True
        for key, check in self.checks.items():
            if check['required'] and check['status'] not in ['success']:
                ready = False
                break
                
        if ready:
            self.install_button.config(state=tk.NORMAL)
            self.progress_text.set("Ready to install! Click 'Install' to proceed.")
            self.log("System requirements check completed - ready to install!")
        else:
            self.install_button.config(state=tk.DISABLED)
            self.progress_text.set("Missing required dependencies - please install them first")
            self.log("System requirements check completed - missing dependencies", "ERROR")
            self.show_installation_instructions()
            
    def show_installation_instructions(self):
        """Show instructions for installing missing dependencies"""
        instructions = []
        
        if self.checks['git']['status'] != 'success':
            if self.system == 'darwin':
                instructions.append("Install Git: brew install git")
            elif self.system == 'linux':
                instructions.append("Install Git: sudo apt-get install git")
            elif self.system == 'windows':
                instructions.append("Install Git: Download from https://git-scm.com/")
                
        if self.checks['gource']['status'] != 'success':
            if self.system == 'darwin':
                instructions.append("Install Gource: brew install gource")
            elif self.system == 'linux':
                instructions.append("Install Gource: sudo apt-get install gource")
            elif self.system == 'windows':
                instructions.append("Install Gource: Download from https://gource.io/")
                
        if instructions:
            self.log("Installation instructions:", "INFO")
            for instruction in instructions:
                self.log(f"  • {instruction}", "INFO")
                
    def start_installation(self):
        """Start the installation process"""
        if self.installation_thread and self.installation_thread.is_alive():
            return
            
        self.installation_cancelled = False
        self.install_button.config(state=tk.DISABLED)
        self.cancel_button.config(text="Cancel", state=tk.NORMAL)
        
        def install_thread():
            self.perform_installation()
            
        self.installation_thread = threading.Thread(target=install_thread, daemon=True)
        self.installation_thread.start()
        
    def perform_installation(self):
        """Perform the actual installation"""
        try:
            self.root.after(0, lambda: self.progress_text.set("Installing Python dependencies..."))
            self.root.after(0, lambda: self.progress_var.set(20))
            
            # Install Python dependencies
            self.update_requirement_status('python_deps', 'checking', 'Installing...')
            self.log("Installing Python dependencies...")
            
            requirements_file = self.project_dir / "requirements.txt"
            if requirements_file.exists():
                cmd = [sys.executable, "-m", "pip", "install", "-r", str(requirements_file)]
                result = subprocess.run(cmd, capture_output=True, text=True)
                
                if result.returncode == 0:
                    self.update_requirement_status('python_deps', 'success', 'Installed')
                    self.log("Python dependencies installed successfully")
                else:
                    self.update_requirement_status('python_deps', 'error', 'Failed')
                    self.log(f"Failed to install Python dependencies: {result.stderr}", "ERROR")
                    self.root.after(0, self.installation_failed)
                    return
            else:
                self.log("requirements.txt not found", "ERROR")
                self.root.after(0, self.installation_failed)
                return
                
            if self.installation_cancelled:
                return
                
            self.root.after(0, lambda: self.progress_text.set("Testing installation..."))
            self.root.after(0, lambda: self.progress_var.set(60))
            
            # Test installation
            self.log("Testing installation...")
            cmd = [sys.executable, "-c", "import sys; sys.path.insert(0, '.'); from gui.main_window_with_video import GourceGUIApp; print('Success')"]
            result = subprocess.run(cmd, cwd=self.project_dir, capture_output=True, text=True, timeout=10)
            
            if result.returncode == 0:
                self.log("Installation test passed")
            else:
                self.log(f"Installation test failed: {result.stderr}", "ERROR")
                self.root.after(0, self.installation_failed)
                return
                
            if self.installation_cancelled:
                return
                
            self.root.after(0, lambda: self.progress_text.set("Creating desktop shortcut..."))
            self.root.after(0, lambda: self.progress_var.set(80))
            
            # Create desktop shortcut
            self.create_desktop_shortcut()
            
            self.root.after(0, lambda: self.progress_var.set(100))
            self.root.after(0, self.installation_complete)
            
        except Exception as e:
            self.log(f"Installation failed with error: {e}", "ERROR")
            self.root.after(0, self.installation_failed)
            
    def create_desktop_shortcut(self):
        """Create desktop shortcut"""
        try:
            main_py = self.project_dir / "main.py"
            
            if self.system == "darwin":
                shortcut_path = Path.home() / "Desktop" / "Gource GUI.command"
                shortcut_content = f'''#!/bin/bash
cd "{self.project_dir}"
python3 "{main_py}"
'''
                shortcut_path.write_text(shortcut_content)
                os.chmod(shortcut_path, 0o755)
                self.log(f"Desktop shortcut created: {shortcut_path}")
                
            elif self.system == "linux":
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
                self.log(f"Desktop shortcut created: {shortcut_path}")
                
            elif self.system == "windows":
                shortcut_path = Path.home() / "Desktop" / "Gource GUI.bat"
                shortcut_content = f'''@echo off
cd /d "{self.project_dir}"
python "{main_py}"
pause
'''
                shortcut_path.write_text(shortcut_content)
                self.log(f"Desktop shortcut created: {shortcut_path}")
                
        except Exception as e:
            self.log(f"Could not create desktop shortcut: {e}", "WARNING")
            
    def installation_complete(self):
        """Handle successful installation completion"""
        self.progress_text.set("Installation completed successfully!")
        self.install_button.config(text="Install", state=tk.DISABLED)
        self.cancel_button.config(text="Close", state=tk.NORMAL)
        self.test_button.config(state=tk.NORMAL)
        
        self.log("=" * 50)
        self.log("INSTALLATION COMPLETE!")
        self.log("=" * 50)
        self.log("You can now:")
        self.log("1. Click 'Test Installation' to verify everything works")
        self.log("2. Use the desktop shortcut to launch Gource GUI")
        self.log(f"3. Run from command line: cd '{self.project_dir}' && python3 main.py")
        
        messagebox.showinfo(
            "Installation Complete",
            "Gource GUI has been installed successfully!\n\n"
            "• Desktop shortcut created\n"
            "• All dependencies verified\n"
            "• Ready to use!\n\n"
            "Click 'Test Installation' to verify everything works."
        )
        
    def installation_failed(self):
        """Handle installation failure"""
        self.progress_text.set("Installation failed - see log for details")
        self.install_button.config(text="Retry", state=tk.NORMAL)
        self.cancel_button.config(text="Close", state=tk.NORMAL)
        
        messagebox.showerror(
            "Installation Failed",
            "Installation failed. Please check the log for details.\n\n"
            "You may need to install missing system dependencies manually."
        )
        
    def cancel_installation(self):
        """Cancel installation or close window"""
        if self.cancel_button.cget('text') == 'Cancel' and self.installation_thread and self.installation_thread.is_alive():
            self.installation_cancelled = True
            self.log("Installation cancelled by user")
            self.progress_text.set("Installation cancelled")
            self.install_button.config(state=tk.NORMAL)
            self.cancel_button.config(text="Close")
        else:
            self.root.quit()
            
    def test_installation(self):
        """Test the installation by running the main application"""
        try:
            main_py = self.project_dir / "main.py"
            if main_py.exists():
                self.log("Launching Gource GUI for testing...")
                if self.system == "windows":
                    subprocess.Popen([sys.executable, str(main_py)], cwd=self.project_dir)
                else:
                    subprocess.Popen([sys.executable, str(main_py)], cwd=self.project_dir)
                messagebox.showinfo("Test", "Gource GUI should now be starting...")
            else:
                messagebox.showerror("Error", f"main.py not found at {main_py}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to launch Gource GUI: {e}")
            
    def show_help(self):
        """Show help dialog"""
        help_text = """
Gource GUI Installer Help

This installer will:
1. Check system requirements
2. Install Python dependencies
3. Create desktop shortcuts
4. Test the installation

Requirements:
• Python 3.7+ with tkinter
• Git (version control)
• Gource (visualization tool)
• FFmpeg (optional, for video export)

Troubleshooting:
• If requirements are missing, install them using your system's package manager
• On macOS: Use Homebrew (brew install <package>)
• On Linux: Use apt-get or your distribution's package manager
• On Windows: Download installers from official websites

For more help, visit:
https://github.com/tkosin/Gource-GUI
        """
        
        help_window = tk.Toplevel(self.root)
        help_window.title("Help")
        help_window.geometry("600x400")
        help_window.transient(self.root)
        
        text_widget = scrolledtext.ScrolledText(help_window, wrap=tk.WORD, padx=10, pady=10)
        text_widget.pack(fill=tk.BOTH, expand=True)
        text_widget.insert(tk.END, help_text)
        text_widget.config(state=tk.DISABLED)
        
        close_button = ttk.Button(help_window, text="Close", command=help_window.destroy)
        close_button.pack(pady=10)
        
    def run(self):
        """Run the installer GUI"""
        self.root.protocol("WM_DELETE_WINDOW", self.cancel_installation)
        self.root.mainloop()

def main():
    """Main function"""
    try:
        installer = GourceGUIInstallerWindow()
        installer.run()
    except KeyboardInterrupt:
        print("\nInstaller cancelled by user.")
    except Exception as e:
        messagebox.showerror("Error", f"Installer failed to start: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
