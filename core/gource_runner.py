"""Gource command runner and process management"""
import os
import subprocess
import sys
import platform
from typing import List, Dict, Any, Optional, Callable
import threading
import queue

class GourceRunner:
    """Handles running Gource with various configuration options"""
    
    def __init__(self):
        self.process = None
        self.is_running = False
        
    def check_gource_installed(self) -> bool:
        """Check if Gource is installed and accessible"""
        try:
            result = subprocess.run(['gource', '--help'], 
                                  capture_output=True, 
                                  timeout=5)
            return result.returncode == 0
        except (FileNotFoundError, subprocess.TimeoutExpired):
            return False
    
    def get_installation_instructions(self) -> str:
        """Get platform-specific installation instructions for Gource"""
        system = platform.system().lower()
        
        instructions = {
            'darwin': '''To install Gource on macOS:
            
Option 1 - Homebrew (recommended):
  brew install gource

Option 2 - MacPorts:
  sudo port install gource

Option 3 - Build from source:
  Download from: https://gource.io''',
            
            'linux': '''To install Gource on Linux:
            
Ubuntu/Debian:
  sudo apt-get install gource

Fedora/RHEL:
  sudo dnf install gource

Arch Linux:
  sudo pacman -S gource

Or build from source: https://gource.io''',
            
            'windows': '''To install Gource on Windows:
            
Option 1 - Download installer:
  https://gource.io/downloads/

Option 2 - Using Chocolatey:
  choco install gource

Option 3 - Using vcpkg:
  vcpkg install gource'''
        }
        
        return instructions.get(system, 'Please visit https://gource.io for installation instructions.')
    
    def build_command(self, repo_path: str, settings: Dict[str, Any]) -> List[str]:
        """Build Gource command from settings"""
        cmd = ['gource']
        
        # Repository path
        cmd.append(repo_path)
        
        # Resolution
        resolution = settings.get('resolution', '1280x720')
        if resolution == 'custom':
            width = settings.get('custom_width', 1920)
            height = settings.get('custom_height', 1080)
            cmd.extend(['--viewport', f'{width}x{height}'])
        elif resolution != 'default':
            cmd.extend(['--viewport', resolution])
        
        # Fullscreen
        if settings.get('fullscreen', False):
            cmd.append('--fullscreen')
        
        # Time settings
        seconds_per_day = settings.get('seconds_per_day', 10.0)
        if seconds_per_day != 10.0:
            cmd.extend(['--seconds-per-day', str(seconds_per_day)])
        
        auto_skip = settings.get('auto_skip_seconds', 3.0)
        if auto_skip != 3.0:
            cmd.extend(['--auto-skip-seconds', str(auto_skip)])
        
        # Date range
        start_date = settings.get('start_date', '').strip()
        if start_date:
            cmd.extend(['--start-date', start_date])
        
        stop_date = settings.get('stop_date', '').strip()
        if stop_date:
            cmd.extend(['--stop-date', stop_date])
        
        # Hide elements
        hide_elements = []
        if settings.get('hide_filenames', False):
            hide_elements.append('filenames')
        if settings.get('hide_dirnames', False):
            hide_elements.append('dirnames')
        if settings.get('hide_usernames', False):
            hide_elements.append('usernames')
        if settings.get('hide_bloom', False):
            hide_elements.append('bloom')
        if settings.get('hide_progress', False):
            hide_elements.append('progress')
        
        if hide_elements:
            cmd.extend(['--hide', ','.join(hide_elements)])
        
        # Background color
        bg_color = settings.get('background_color', '').strip()
        if bg_color and bg_color != '#000000':
            # Remove # if present
            if bg_color.startswith('#'):
                bg_color = bg_color[1:]
            cmd.extend(['--background-colour', bg_color])
        
        # Font scale
        font_scale = settings.get('font_scale', 1.0)
        if font_scale != 1.0:
            cmd.extend(['--font-scale', str(font_scale)])
        
        # Camera mode
        camera_mode = settings.get('camera_mode', 'overview')
        if camera_mode != 'overview':
            cmd.extend(['--camera-mode', camera_mode])
        
        # User images
        user_image_dir = settings.get('user_image_dir', '').strip()
        if user_image_dir and os.path.exists(user_image_dir):
            cmd.extend(['--user-image-dir', user_image_dir])
        
        # Elasticity
        elasticity = settings.get('elasticity', 0.0)
        if elasticity != 0.0:
            cmd.extend(['--elasticity', str(elasticity)])
        
        # Performance settings
        if settings.get('multi_sampling', False):
            cmd.append('--multi-sampling')
        
        # Framerate (for video output)
        framerate = settings.get('framerate', 60)
        if framerate != 60:
            cmd.extend(['--output-framerate', str(framerate)])
        
        return cmd
    
    def run_gource(self, repo_path: str, settings: Dict[str, Any], 
                   output_callback: Optional[Callable[[str], None]] = None,
                   error_callback: Optional[Callable[[str], None]] = None) -> bool:
        """Run Gource with given settings"""
        
        if not self.check_gource_installed():
            if error_callback:
                error_callback("Gource is not installed or not found in PATH")
            return False
        
        if self.is_running:
            if error_callback:
                error_callback("Gource is already running")
            return False
        
        try:
            cmd = self.build_command(repo_path, settings)
            
            if output_callback:
                output_callback(f"Running command: {' '.join(cmd)}")
            
            # Start the process
            self.process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                cwd=repo_path
            )
            
            self.is_running = True
            
            # Start threads to handle output
            if output_callback or error_callback:
                threading.Thread(
                    target=self._handle_process_output,
                    args=(output_callback, error_callback),
                    daemon=True
                ).start()
            
            return True
            
        except Exception as e:
            if error_callback:
                error_callback(f"Failed to start Gource: {str(e)}")
            return False
    
    def run_gource_video_export(self, repo_path: str, settings: Dict[str, Any], 
                               output_file: str,
                               progress_callback: Optional[Callable[[str], None]] = None,
                               error_callback: Optional[Callable[[str], None]] = None) -> bool:
        """Run Gource with video export"""
        
        if not self.check_gource_installed():
            if error_callback:
                error_callback("Gource is not installed or not found in PATH")
            return False
        
        try:
            cmd = self.build_command(repo_path, settings)
            
            # Add video export options
            cmd.extend(['--output-ppm-stream', '-'])
            cmd.extend(['--stop-at-end'])
            
            # Check if ffmpeg is available for video encoding
            if not self._check_ffmpeg():
                if error_callback:
                    error_callback("FFmpeg is required for video export but was not found")
                return False
            
            # Build ffmpeg command
            ffmpeg_cmd = [
                'ffmpeg', '-y', '-r', str(settings.get('framerate', 60)),
                '-f', 'image2pipe', '-vcodec', 'ppm', '-i', '-',
                '-vcodec', 'libx264', '-preset', 'medium',
                '-pix_fmt', 'yuv420p', '-crf', '18',
                '-movflags', 'faststart',
                output_file
            ]
            
            if progress_callback:
                progress_callback(f"Starting video export to: {output_file}")
            
            # Start both processes with pipe connection
            gource_process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=repo_path)
            ffmpeg_process = subprocess.Popen(ffmpeg_cmd, stdin=gource_process.stdout, stderr=subprocess.PIPE)
            
            gource_process.stdout.close()  # Allow gource to receive SIGPIPE if ffmpeg exits
            
            # Wait for completion
            ffmpeg_process.wait()
            gource_process.wait()
            
            if ffmpeg_process.returncode == 0:
                if progress_callback:
                    progress_callback(f"Video export completed: {output_file}")
                return True
            else:
                if error_callback:
                    _, stderr = ffmpeg_process.communicate()
                    error_callback(f"Video export failed: {stderr.decode()}")
                return False
                
        except Exception as e:
            if error_callback:
                error_callback(f"Video export failed: {str(e)}")
            return False
    
    def stop_gource(self) -> bool:
        """Stop the running Gource process"""
        if self.process and self.is_running:
            try:
                self.process.terminate()
                self.process.wait(timeout=5)
                return True
            except subprocess.TimeoutExpired:
                self.process.kill()
                return True
            except Exception:
                return False
            finally:
                self.is_running = False
                self.process = None
        return True
    
    def _handle_process_output(self, output_callback: Optional[Callable[[str], None]], 
                              error_callback: Optional[Callable[[str], None]]) -> None:
        """Handle process output in separate thread"""
        try:
            # Read stderr for error messages
            while self.process and self.process.poll() is None:
                if self.process.stderr:
                    line = self.process.stderr.readline()
                    if line and error_callback:
                        error_callback(line.strip())
            
            # Get final return code
            if self.process:
                return_code = self.process.poll()
                if return_code == 0 and output_callback:
                    output_callback("Gource completed successfully")
                elif return_code != 0 and error_callback:
                    error_callback(f"Gource exited with code {return_code}")
                    
        except Exception as e:
            if error_callback:
                error_callback(f"Error handling process output: {str(e)}")
        finally:
            self.is_running = False
    
    def _check_ffmpeg(self) -> bool:
        """Check if FFmpeg is installed"""
        try:
            subprocess.run(['ffmpeg', '-version'], 
                         capture_output=True, 
                         timeout=5)
            return True
        except (FileNotFoundError, subprocess.TimeoutExpired):
            return False
