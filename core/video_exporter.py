"""Video export functionality for Gource GUI"""
import os
import subprocess
import threading
from typing import Optional, Callable, Dict, Any

class VideoExporter:
    """Handles video export functionality for Gource visualizations"""
    
    def __init__(self):
        self.is_exporting = False
        self.current_process = None
        
    def check_ffmpeg_installed(self) -> bool:
        """Check if FFmpeg is installed and accessible"""
        try:
            result = subprocess.run(['ffmpeg', '-version'], 
                                  capture_output=True, 
                                  timeout=5)
            return result.returncode == 0
        except (FileNotFoundError, subprocess.TimeoutExpired):
            return False
    
    def get_ffmpeg_installation_instructions(self) -> str:
        """Get platform-specific FFmpeg installation instructions"""
        return """To install FFmpeg:

macOS:
  brew install ffmpeg

Linux (Ubuntu/Debian):
  sudo apt-get install ffmpeg

Linux (Fedora/RHEL):
  sudo dnf install ffmpeg

Windows:
  Download from: https://ffmpeg.org/download.html
  Or use chocolatey: choco install ffmpeg

FFmpeg is required for video export functionality."""
    
    def get_supported_formats(self) -> Dict[str, str]:
        """Get supported video formats"""
        return {
            "MP4 (H.264)": "mp4",
            "MOV (QuickTime)": "mov", 
            "AVI": "avi",
            "WebM": "webm"
        }
    
    def get_quality_presets(self) -> Dict[str, Dict[str, Any]]:
        """Get quality presets for video export"""
        return {
            "Ultra High (CRF 15)": {"crf": "15", "preset": "slow"},
            "High (CRF 18)": {"crf": "18", "preset": "medium"},
            "Medium (CRF 23)": {"crf": "23", "preset": "medium"},
            "Low (CRF 28)": {"crf": "28", "preset": "fast"}
        }
    
    def export_video(self, 
                    gource_command: list,
                    output_path: str,
                    quality_preset: str = "High (CRF 18)",
                    framerate: int = 60,
                    progress_callback: Optional[Callable[[str], None]] = None,
                    error_callback: Optional[Callable[[str], None]] = None,
                    completion_callback: Optional[Callable[[bool, str], None]] = None) -> bool:
        """Export Gource visualization to video file"""
        
        if self.is_exporting:
            if error_callback:
                error_callback("Video export already in progress")
            return False
        
        if not self.check_ffmpeg_installed():
            if error_callback:
                error_callback("FFmpeg is not installed. " + self.get_ffmpeg_installation_instructions())
            return False
        
        # Start export in background thread
        export_thread = threading.Thread(
            target=self._export_video_thread,
            args=(gource_command, output_path, quality_preset, framerate, 
                  progress_callback, error_callback, completion_callback),
            daemon=True
        )
        export_thread.start()
        
        return True
    
    def _export_video_thread(self,
                           gource_command: list,
                           output_path: str,
                           quality_preset: str,
                           framerate: int,
                           progress_callback: Optional[Callable[[str], None]],
                           error_callback: Optional[Callable[[str], None]],
                           completion_callback: Optional[Callable[[bool, str], None]]):
        """Export video in background thread"""
        
        self.is_exporting = True
        
        try:
            if progress_callback:
                progress_callback("Starting video export...")
            
            # Get quality settings
            quality_presets = self.get_quality_presets()
            quality_settings = quality_presets.get(quality_preset, quality_presets["High (CRF 18)"])
            
            # Modify Gource command for video export
            gource_cmd = gource_command.copy()
            gource_cmd.extend([
                '--output-ppm-stream', '-',
                '--stop-at-end'
            ])
            
            # Build FFmpeg command
            ffmpeg_cmd = [
                'ffmpeg', '-y',  # Overwrite output file
                '-r', str(framerate),  # Input framerate
                '-f', 'image2pipe',
                '-vcodec', 'ppm',
                '-i', '-',  # Read from stdin
                '-vcodec', 'libx264',
                '-preset', quality_settings['preset'],
                '-crf', quality_settings['crf'],
                '-pix_fmt', 'yuv420p',
                '-movflags', 'faststart',
                output_path
            ]
            
            if progress_callback:
                progress_callback("Launching Gource and FFmpeg...")
            
            # Start Gource process
            gource_process = subprocess.Popen(
                gource_cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=False  # Binary mode for PPM stream
            )
            
            # Start FFmpeg process
            ffmpeg_process = subprocess.Popen(
                ffmpeg_cmd,
                stdin=gource_process.stdout,
                stderr=subprocess.PIPE,
                text=True
            )
            
            # Close Gource stdout in parent process
            gource_process.stdout.close()
            
            # Store processes for potential cancellation
            self.current_process = (gource_process, ffmpeg_process)
            
            if progress_callback:
                progress_callback("Rendering video... This may take several minutes.")
            
            # Monitor FFmpeg stderr for progress (optional)
            ffmpeg_stderr_thread = threading.Thread(
                target=self._monitor_ffmpeg_progress,
                args=(ffmpeg_process, progress_callback),
                daemon=True
            )
            ffmpeg_stderr_thread.start()
            
            # Wait for both processes to complete
            gource_return_code = gource_process.wait()
            ffmpeg_return_code = ffmpeg_process.wait()
            
            # Check results
            if ffmpeg_return_code == 0:
                if progress_callback:
                    progress_callback("Video export completed successfully!")
                if completion_callback:
                    completion_callback(True, f"Video exported to: {output_path}")
            else:
                # Get FFmpeg error output
                _, ffmpeg_stderr = ffmpeg_process.communicate()
                error_msg = f"FFmpeg failed with code {ffmpeg_return_code}: {ffmpeg_stderr}"
                
                if error_callback:
                    error_callback(error_msg)
                if completion_callback:
                    completion_callback(False, error_msg)
            
        except Exception as e:
            error_msg = f"Video export failed: {str(e)}"
            if error_callback:
                error_callback(error_msg)
            if completion_callback:
                completion_callback(False, error_msg)
        
        finally:
            self.is_exporting = False
            self.current_process = None
    
    def _monitor_ffmpeg_progress(self, 
                               ffmpeg_process: subprocess.Popen,
                               progress_callback: Optional[Callable[[str], None]]):
        """Monitor FFmpeg stderr for progress information"""
        if not progress_callback or not ffmpeg_process.stderr:
            return
        
        try:
            while ffmpeg_process.poll() is None:
                line = ffmpeg_process.stderr.readline()
                if line:
                    # Look for time information in FFmpeg output
                    if "time=" in line:
                        # Extract time information
                        time_part = line.split("time=")[1].split()[0]
                        progress_callback(f"Rendering... Time: {time_part}")
        except Exception:
            # Ignore errors in progress monitoring
            pass
    
    def cancel_export(self) -> bool:
        """Cancel ongoing video export"""
        if not self.is_exporting or not self.current_process:
            return False
        
        try:
            gource_process, ffmpeg_process = self.current_process
            
            # Terminate processes
            if gource_process and gource_process.poll() is None:
                gource_process.terminate()
            
            if ffmpeg_process and ffmpeg_process.poll() is None:
                ffmpeg_process.terminate()
            
            # Wait a bit and force kill if necessary
            import time
            time.sleep(2)
            
            if gource_process and gource_process.poll() is None:
                gource_process.kill()
                
            if ffmpeg_process and ffmpeg_process.poll() is None:
                ffmpeg_process.kill()
            
            self.is_exporting = False
            self.current_process = None
            return True
            
        except Exception:
            return False
