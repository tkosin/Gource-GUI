"""Main window for Gource GUI application"""
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import os
from typing import Optional

class GourceGUIApp:
    """Main application window for Gource GUI"""
    
    def __init__(self, root: tk.Tk):
        self.root = root
        self.current_repo_path = ""
        self._setup_basic_ui()
    
    def _setup_basic_ui(self):
        """Set up basic user interface"""
        self.root.title("Gource GUI - Version Control Visualization")
        
        # Create main container
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Repository selection
        repo_frame = ttk.LabelFrame(main_frame, text="Repository Selection", padding=10)
        repo_frame.pack(fill=tk.X, pady=(0, 10))
        
        path_frame = ttk.Frame(repo_frame)
        path_frame.pack(fill=tk.X)
        
        ttk.Label(path_frame, text="Repository Path:").pack(side=tk.LEFT)
        
        self.repo_path_var = tk.StringVar()
        self.path_entry = ttk.Entry(path_frame, textvariable=self.repo_path_var)
        self.path_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(5, 5))
        
        ttk.Button(path_frame, text="Browse...", command=self._browse_repository).pack(side=tk.RIGHT)
        
        # Status
        self.status_label = ttk.Label(repo_frame, text="No repository selected")
        self.status_label.pack(pady=(10, 0))
        
        # Settings notebook
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True, pady=(10, 0))
        
        # Basic settings tab
        settings_frame = ttk.Frame(self.notebook)
        self.notebook.add(settings_frame, text="Settings")
        
        # Resolution setting
        ttk.Label(settings_frame, text="Resolution:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.resolution_var = tk.StringVar(value="1280x720")
        resolution_combo = ttk.Combobox(settings_frame, textvariable=self.resolution_var, 
                                       values=["640x480", "1280x720", "1920x1080"])
        resolution_combo.grid(row=0, column=1, sticky=tk.W, padx=(10, 0))
        
        # Seconds per day
        ttk.Label(settings_frame, text="Seconds per Day:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.seconds_var = tk.DoubleVar(value=10.0)
        seconds_spin = ttk.Spinbox(settings_frame, from_=0.1, to=60.0, increment=0.1, 
                                  textvariable=self.seconds_var, width=10)
        seconds_spin.grid(row=1, column=1, sticky=tk.W, padx=(10, 0))
        
        # Fullscreen option
        self.fullscreen_var = tk.BooleanVar()
        ttk.Checkbutton(settings_frame, text="Fullscreen", 
                       variable=self.fullscreen_var).grid(row=2, column=0, sticky=tk.W, pady=5)
        
        # Action buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=(10, 0))
        
        self.run_button = ttk.Button(button_frame, text="Run Gource", command=self._run_gource)
        self.run_button.pack(side=tk.RIGHT, padx=(5, 0))
        
        # Status bar
        self.status_bar = ttk.Label(self.root, text="Ready", relief=tk.SUNKEN)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
    
    def _browse_repository(self):
        """Browse for repository folder"""
        repo_path = filedialog.askdirectory(title="Select Git Repository Folder")
        if repo_path:
            self.repo_path_var.set(repo_path)
            self.current_repo_path = repo_path
            self.status_label.config(text=f"Repository: {os.path.basename(repo_path)}")
    
    def _run_gource(self):
        """Run Gource with current settings"""
        if not self.current_repo_path:
            messagebox.showwarning("No Repository", "Please select a repository first.")
            return
        
        # Build command
        cmd = ["gource", self.current_repo_path]
        
        # Add resolution
        resolution = self.resolution_var.get()
        if resolution:
            cmd.extend(["--viewport", resolution])
        
        # Add seconds per day
        seconds = self.seconds_var.get()
        if seconds != 10.0:
            cmd.extend(["--seconds-per-day", str(seconds)])
        
        # Add fullscreen
        if self.fullscreen_var.get():
            cmd.append("--fullscreen")
        
        # Show command and run
        command_str = " ".join(cmd)
        self.status_bar.config(text=f"Running: {command_str}")
        
        try:
            import subprocess
            subprocess.Popen(cmd, cwd=self.current_repo_path)
            messagebox.showinfo("Success", "Gource started successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to run Gource:\n{str(e)}")
        
        self.status_bar.config(text="Ready")
