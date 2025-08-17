"""Enhanced main window for Gource GUI with video export functionality"""
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import os
import threading
from typing import Optional

from core.gource_runner import GourceRunner
from core.video_exporter import VideoExporter

class GourceGUIApp:
    """Main application window for Gource GUI with video export"""
    
    def __init__(self, root: tk.Tk):
        self.root = root
        self.runner = GourceRunner()
        self.video_exporter = VideoExporter()
        self.current_repo_path = ""
        self._setup_ui()
    
    def _setup_ui(self):
        """Set up the enhanced user interface"""
        self.root.title("Gource GUI - Version Control Visualization")
        
        # Create main container
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Repository selection
        self._create_repo_selection(main_frame)
        
        # Settings notebook
        self._create_settings_notebook(main_frame)
        
        # Action buttons
        self._create_action_buttons(main_frame)
        
        # Progress bar (initially hidden)
        self._create_progress_bar(main_frame)
        
        # Status bar
        self._create_status_bar()
        
        # Check dependencies on startup
        self._check_dependencies()
    
    def _create_repo_selection(self, parent):
        """Create repository selection widgets"""
        repo_frame = ttk.LabelFrame(parent, text="Repository Selection", padding=10)
        repo_frame.pack(fill=tk.X, pady=(0, 10))
        
        path_frame = ttk.Frame(repo_frame)
        path_frame.pack(fill=tk.X)
        
        ttk.Label(path_frame, text="Repository Path:").pack(side=tk.LEFT)
        
        self.repo_path_var = tk.StringVar()
        self.repo_path_var.trace_add('write', self._on_repo_path_changed)
        
        self.path_entry = ttk.Entry(path_frame, textvariable=self.repo_path_var)
        self.path_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(5, 5))
        
        ttk.Button(path_frame, text="Browse...", command=self._browse_repository).pack(side=tk.RIGHT)
        
        # Status
        self.status_label = ttk.Label(repo_frame, text="No repository selected")
        self.status_label.pack(pady=(10, 0))
    
    def _create_settings_notebook(self, parent):
        """Create settings notebook with multiple tabs"""
        self.notebook = ttk.Notebook(parent)
        self.notebook.pack(fill=tk.BOTH, expand=True, pady=(10, 0))
        
        # Basic settings tab
        self._create_basic_settings_tab()
        
        # Video export tab
        self._create_video_export_tab()
    
    def _create_basic_settings_tab(self):
        """Create basic settings tab"""
        settings_frame = ttk.Frame(self.notebook)
        self.notebook.add(settings_frame, text="Basic Settings")
        
        # Create a scrollable frame
        canvas = tk.Canvas(settings_frame)
        scrollbar = ttk.Scrollbar(settings_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Resolution setting
        ttk.Label(scrollable_frame, text="Resolution:").grid(row=0, column=0, sticky=tk.W, pady=5, padx=5)
        self.resolution_var = tk.StringVar(value="1280x720")
        resolution_combo = ttk.Combobox(scrollable_frame, textvariable=self.resolution_var, 
                                       values=["640x480", "1280x720", "1920x1080", "custom"])
        resolution_combo.grid(row=0, column=1, sticky=tk.W, padx=(10, 5))
        
        # Custom resolution (only shown when custom is selected)
        self.custom_res_frame = ttk.Frame(scrollable_frame)
        self.custom_res_frame.grid(row=1, column=0, columnspan=2, sticky=tk.W, padx=5)
        
        ttk.Label(self.custom_res_frame, text="Width:").pack(side=tk.LEFT)
        self.custom_width_var = tk.IntVar(value=1920)
        ttk.Entry(self.custom_res_frame, textvariable=self.custom_width_var, width=8).pack(side=tk.LEFT, padx=5)
        
        ttk.Label(self.custom_res_frame, text="Height:").pack(side=tk.LEFT, padx=(10, 0))
        self.custom_height_var = tk.IntVar(value=1080)
        ttk.Entry(self.custom_res_frame, textvariable=self.custom_height_var, width=8).pack(side=tk.LEFT, padx=5)
        
        # Hide custom resolution initially
        self.custom_res_frame.grid_remove()
        
        # Bind resolution change
        resolution_combo.bind('<<ComboboxSelected>>', self._on_resolution_changed)
        
        # Seconds per day
        ttk.Label(scrollable_frame, text="Seconds per Day:").grid(row=2, column=0, sticky=tk.W, pady=5, padx=5)
        self.seconds_var = tk.DoubleVar(value=10.0)
        seconds_spin = ttk.Spinbox(scrollable_frame, from_=0.1, to=60.0, increment=0.1, 
                                  textvariable=self.seconds_var, width=10)
        seconds_spin.grid(row=2, column=1, sticky=tk.W, padx=(10, 5))
        
        # Auto skip seconds
        ttk.Label(scrollable_frame, text="Auto Skip (seconds):").grid(row=3, column=0, sticky=tk.W, pady=5, padx=5)
        self.auto_skip_var = tk.DoubleVar(value=3.0)
        ttk.Spinbox(scrollable_frame, from_=0.0, to=30.0, increment=0.5,
                   textvariable=self.auto_skip_var, width=10).grid(row=3, column=1, sticky=tk.W, padx=(10, 5))
        
        # Display options
        ttk.Label(scrollable_frame, text="Display Options:").grid(row=4, column=0, sticky=tk.W, pady=(15, 5), padx=5)
        
        self.fullscreen_var = tk.BooleanVar()
        ttk.Checkbutton(scrollable_frame, text="Fullscreen", 
                       variable=self.fullscreen_var).grid(row=5, column=0, sticky=tk.W, pady=2, padx=20)
        
        self.hide_filenames_var = tk.BooleanVar()
        ttk.Checkbutton(scrollable_frame, text="Hide Filenames", 
                       variable=self.hide_filenames_var).grid(row=6, column=0, sticky=tk.W, pady=2, padx=20)
        
        self.hide_usernames_var = tk.BooleanVar()
        ttk.Checkbutton(scrollable_frame, text="Hide Usernames", 
                       variable=self.hide_usernames_var).grid(row=7, column=0, sticky=tk.W, pady=2, padx=20)
        
        self.hide_dirnames_var = tk.BooleanVar()
        ttk.Checkbutton(scrollable_frame, text="Hide Directory Names", 
                       variable=self.hide_dirnames_var).grid(row=8, column=0, sticky=tk.W, pady=2, padx=20)
        
        # Background color
        ttk.Label(scrollable_frame, text="Background Color:").grid(row=9, column=0, sticky=tk.W, pady=(15, 5), padx=5)
        self.bg_color_var = tk.StringVar(value="#000000")
        bg_color_frame = ttk.Frame(scrollable_frame)
        bg_color_frame.grid(row=9, column=1, sticky=tk.W, padx=(10, 5))
        
        self.bg_color_entry = ttk.Entry(bg_color_frame, textvariable=self.bg_color_var, width=10)
        self.bg_color_entry.pack(side=tk.LEFT)
        
        ttk.Button(bg_color_frame, text="Pick Color", command=self._pick_color).pack(side=tk.LEFT, padx=(5, 0))
        
        # Pack scrollable frame
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
    
    def _create_video_export_tab(self):
        """Create video export settings tab"""
        video_frame = ttk.Frame(self.notebook)
        self.notebook.add(video_frame, text="Video Export")
        
        # Check FFmpeg status
        ffmpeg_frame = ttk.LabelFrame(video_frame, text="FFmpeg Status", padding=10)
        ffmpeg_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.ffmpeg_status_label = ttk.Label(ffmpeg_frame, text="Checking FFmpeg...")
        self.ffmpeg_status_label.pack(anchor=tk.W)
        
        # Output settings
        output_frame = ttk.LabelFrame(video_frame, text="Output Settings", padding=10)
        output_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Output path
        ttk.Label(output_frame, text="Output File:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.output_path_var = tk.StringVar()
        
        path_frame = ttk.Frame(output_frame)
        path_frame.grid(row=0, column=1, sticky=tk.EW, pady=5, padx=(10, 0))
        path_frame.columnconfigure(0, weight=1)
        
        self.output_path_entry = ttk.Entry(path_frame, textvariable=self.output_path_var)
        self.output_path_entry.grid(row=0, column=0, sticky=tk.EW, padx=(0, 5))
        
        ttk.Button(path_frame, text="Browse...", command=self._browse_output_file).grid(row=0, column=1)
        
        # Format selection
        ttk.Label(output_frame, text="Format:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.format_var = tk.StringVar(value="MP4 (H.264)")
        format_combo = ttk.Combobox(output_frame, textvariable=self.format_var, 
                                   values=list(self.video_exporter.get_supported_formats().keys()),
                                   state="readonly")
        format_combo.grid(row=1, column=1, sticky=tk.W, pady=5, padx=(10, 0))
        
        # Quality settings
        ttk.Label(output_frame, text="Quality:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.quality_var = tk.StringVar(value="High (CRF 18)")
        quality_combo = ttk.Combobox(output_frame, textvariable=self.quality_var,
                                    values=list(self.video_exporter.get_quality_presets().keys()),
                                    state="readonly")
        quality_combo.grid(row=2, column=1, sticky=tk.W, pady=5, padx=(10, 0))
        
        # Framerate
        ttk.Label(output_frame, text="Framerate:").grid(row=3, column=0, sticky=tk.W, pady=5)
        self.framerate_var = tk.IntVar(value=60)
        ttk.Spinbox(output_frame, from_=15, to=120, increment=5,
                   textvariable=self.framerate_var, width=10).grid(row=3, column=1, sticky=tk.W, pady=5, padx=(10, 0))
        
        # Configure grid weights
        output_frame.columnconfigure(1, weight=1)
    
    def _create_action_buttons(self, parent):
        """Create action buttons"""
        button_frame = ttk.Frame(parent)
        button_frame.pack(fill=tk.X, pady=(10, 0))
        
        # Left side buttons
        left_buttons = ttk.Frame(button_frame)
        left_buttons.pack(side=tk.LEFT)
        
        self.preview_button = ttk.Button(left_buttons, text="Preview Command", 
                                        command=self._preview_command)
        self.preview_button.pack(side=tk.LEFT, padx=(0, 5))
        
        # Right side buttons
        right_buttons = ttk.Frame(button_frame)
        right_buttons.pack(side=tk.RIGHT)
        
        # Video export buttons
        self.export_button = ttk.Button(right_buttons, text="Export Video", 
                                       command=self._export_video)
        self.export_button.pack(side=tk.RIGHT, padx=(5, 0))
        
        self.cancel_export_button = ttk.Button(right_buttons, text="Cancel Export", 
                                              command=self._cancel_export, state=tk.DISABLED)
        self.cancel_export_button.pack(side=tk.RIGHT, padx=(5, 0))
        
        # Run Gource button
        self.run_button = ttk.Button(right_buttons, text="Run Gource", 
                                    command=self._run_gource)
        self.run_button.pack(side=tk.RIGHT, padx=(5, 0))
    
    def _create_progress_bar(self, parent):
        """Create progress bar for video export"""
        self.progress_frame = ttk.Frame(parent)
        # Initially hidden
        
        self.progress_label = ttk.Label(self.progress_frame, text="Export Progress:")
        self.progress_label.pack(anchor=tk.W)
        
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(self.progress_frame, mode='indeterminate')
        self.progress_bar.pack(fill=tk.X, pady=(5, 0))
        
        self.progress_text = ttk.Label(self.progress_frame, text="")
        self.progress_text.pack(anchor=tk.W, pady=(5, 0))
    
    def _create_status_bar(self):
        """Create status bar and footer"""
        # Footer with credits
        footer_frame = ttk.Frame(self.root)
        footer_frame.pack(side=tk.BOTTOM, fill=tk.X, pady=(5, 0))
        
        # Separator line
        ttk.Separator(footer_frame, orient='horizontal').pack(fill=tk.X, pady=(0, 5))
        
        # Credits label
        credits_label = ttk.Label(
            footer_frame, 
            text="Created by Yod Kosin and https://www.letsrover.ai",
            font=('TkDefaultFont', 8),
            foreground='gray'
        )
        credits_label.pack(pady=(0, 5))
        
        # Status bar
        self.status_bar = ttk.Label(self.root, text="Ready", relief=tk.SUNKEN)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
    
    def _check_dependencies(self):
        """Check if required dependencies are installed"""
        # Check Gource
        if self.runner.check_gource_installed():
            gource_status = "✓ Gource installed"
        else:
            gource_status = "✗ Gource not found (install with: brew install gource)"
        
        # Check FFmpeg
        if self.video_exporter.check_ffmpeg_installed():
            ffmpeg_status = "✓ FFmpeg installed - Video export available"
        else:
            ffmpeg_status = "⚠ FFmpeg not found - Video export disabled"
            self.export_button.config(state=tk.DISABLED)
        
        self.ffmpeg_status_label.config(text=ffmpeg_status)
        self._set_status(gource_status)
    
    def _on_resolution_changed(self, event=None):
        """Handle resolution selection change"""
        if self.resolution_var.get() == "custom":
            self.custom_res_frame.grid()
        else:
            self.custom_res_frame.grid_remove()
    
    def _on_repo_path_changed(self, *args):
        """Handle repository path changes"""
        repo_path = self.repo_path_var.get().strip()
        
        if not repo_path:
            self.status_label.config(text="No repository selected")
            return
        
        if os.path.exists(repo_path) and os.path.isdir(repo_path):
            if os.path.exists(os.path.join(repo_path, '.git')):
                self.current_repo_path = repo_path
                repo_name = os.path.basename(repo_path)
                self.status_label.config(text=f"✓ Repository: {repo_name}")
                self._enable_buttons(True)
            else:
                self.status_label.config(text="✗ Not a Git repository")
                self._enable_buttons(False)
        else:
            self.status_label.config(text="✗ Path does not exist")
            self._enable_buttons(False)
    
    def _enable_buttons(self, enable):
        """Enable or disable action buttons"""
        state = tk.NORMAL if enable else tk.DISABLED
        self.preview_button.config(state=state)
        self.run_button.config(state=state)
        
        # Only enable export if FFmpeg is available
        if enable and self.video_exporter.check_ffmpeg_installed():
            self.export_button.config(state=tk.NORMAL)
        else:
            self.export_button.config(state=tk.DISABLED)
    
    def _browse_repository(self):
        """Browse for repository folder"""
        repo_path = filedialog.askdirectory(title="Select Git Repository Folder")
        if repo_path:
            self.repo_path_var.set(repo_path)
    
    def _browse_output_file(self):
        """Browse for output video file location"""
        formats = self.video_exporter.get_supported_formats()
        current_format = formats.get(self.format_var.get(), "mp4")
        
        output_file = filedialog.asksaveasfilename(
            title="Save Video As",
            defaultextension=f".{current_format}",
            filetypes=[
                (f"{self.format_var.get()}", f"*.{current_format}"),
                ("All Files", "*.*")
            ]
        )
        
        if output_file:
            self.output_path_var.set(output_file)
    
    def _pick_color(self):
        """Open color picker dialog"""
        try:
            import tkinter.colorchooser as colorchooser
            color = colorchooser.askcolor(color=self.bg_color_var.get())[1]
            if color:
                self.bg_color_var.set(color)
        except ImportError:
            messagebox.showwarning("Color Picker", "Color picker not available. Please enter hex color manually (e.g., #001122)")
    
    def _get_settings(self):
        """Get current settings from the GUI"""
        settings = {
            'resolution': self.resolution_var.get(),
            'custom_width': self.custom_width_var.get(),
            'custom_height': self.custom_height_var.get(),
            'seconds_per_day': self.seconds_var.get(),
            'auto_skip_seconds': self.auto_skip_var.get(),
            'fullscreen': self.fullscreen_var.get(),
            'hide_filenames': self.hide_filenames_var.get(),
            'hide_usernames': self.hide_usernames_var.get(),
            'hide_dirnames': self.hide_dirnames_var.get(),
            'background_color': self.bg_color_var.get(),
            'framerate': self.framerate_var.get()
        }
        return settings
    
    def _preview_command(self):
        """Preview the Gource command"""
        if not self.current_repo_path:
            messagebox.showwarning("No Repository", "Please select a repository first.")
            return
        
        settings = self._get_settings()
        cmd = self.runner.build_command(self.current_repo_path, settings)
        
        # Show command preview dialog
        dialog = tk.Toplevel(self.root)
        dialog.title("Command Preview")
        dialog.geometry("700x400")
        dialog.transient(self.root)
        
        text_frame = ttk.Frame(dialog)
        text_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        ttk.Label(text_frame, text="Gource Command:").pack(anchor=tk.W)
        
        text_widget = tk.Text(text_frame, wrap=tk.WORD, height=15)
        text_widget.pack(fill=tk.BOTH, expand=True, pady=(5, 0))
        
        scrollbar = ttk.Scrollbar(text_frame, orient=tk.VERTICAL, command=text_widget.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        text_widget.config(yscrollcommand=scrollbar.set)
        
        formatted_cmd = " \\\n  ".join(cmd)
        text_widget.insert(tk.END, formatted_cmd)
        text_widget.config(state=tk.DISABLED)
        
        ttk.Button(dialog, text="Close", command=dialog.destroy).pack(pady=10)
    
    def _run_gource(self):
        """Run Gource with current settings"""
        if not self.current_repo_path:
            messagebox.showwarning("No Repository", "Please select a repository first.")
            return
        
        settings = self._get_settings()
        cmd = self.runner.build_command(self.current_repo_path, settings)
        
        self._set_status(f"Running Gource: {' '.join(cmd[:3])}...")
        
        try:
            import subprocess
            subprocess.Popen(cmd, cwd=self.current_repo_path)
            messagebox.showinfo("Success", "Gource started successfully!")
            self._set_status("Gource visualization started")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to run Gource:\n{str(e)}")
            self._set_status("Failed to start Gource")
    
    def _export_video(self):
        """Export Gource visualization to video"""
        if not self.current_repo_path:
            messagebox.showwarning("No Repository", "Please select a repository first.")
            return
        
        if not self.output_path_var.get():
            messagebox.showwarning("No Output File", "Please specify an output file path.")
            return
        
        # Get settings and build command
        settings = self._get_settings()
        cmd = self.runner.build_command(self.current_repo_path, settings)
        
        # Show progress UI
        self.progress_frame.pack(fill=tk.X, pady=(10, 0))
        self.progress_bar.start()
        
        # Update button states
        self.export_button.config(state=tk.DISABLED)
        self.cancel_export_button.config(state=tk.NORMAL)
        self.run_button.config(state=tk.DISABLED)
        
        # Start export
        success = self.video_exporter.export_video(
            cmd,
            self.output_path_var.get(),
            self.quality_var.get(),
            self.framerate_var.get(),
            progress_callback=self._on_export_progress,
            error_callback=self._on_export_error,
            completion_callback=self._on_export_complete
        )
        
        if not success:
            self._reset_export_ui()
    
    def _cancel_export(self):
        """Cancel ongoing video export"""
        if self.video_exporter.cancel_export():
            self._set_status("Video export cancelled")
            self._reset_export_ui()
        else:
            messagebox.showwarning("Cancel Failed", "Could not cancel the export process.")
    
    def _on_export_progress(self, message):
        """Handle export progress updates"""
        self.root.after(0, lambda: [
            self.progress_text.config(text=message),
            self._set_status(f"Export: {message}")
        ])
    
    def _on_export_error(self, error_message):
        """Handle export errors"""
        self.root.after(0, lambda: [
            messagebox.showerror("Export Error", f"Video export failed:\n\n{error_message}"),
            self._reset_export_ui(),
            self._set_status("Export failed")
        ])
    
    def _on_export_complete(self, success, message):
        """Handle export completion"""
        self.root.after(0, lambda: [
            messagebox.showinfo("Export Complete" if success else "Export Failed", message),
            self._reset_export_ui(),
            self._set_status("Export completed" if success else "Export failed")
        ])
    
    def _reset_export_ui(self):
        """Reset export UI to initial state"""
        self.progress_frame.pack_forget()
        self.progress_bar.stop()
        self.export_button.config(state=tk.NORMAL if self.current_repo_path else tk.DISABLED)
        self.cancel_export_button.config(state=tk.DISABLED)
        self.run_button.config(state=tk.NORMAL if self.current_repo_path else tk.DISABLED)
    
    def _set_status(self, message):
        """Update status bar"""
        self.status_bar.config(text=message)
        self.root.update_idletasks()
