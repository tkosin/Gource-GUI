#!/usr/bin/env python3
"""
Gource GUI - A graphical interface for Gource version control visualization
"""
import sys
import tkinter as tk
from tkinter import messagebox
import traceback

# Add project root to path
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from gui.main_window_with_video import GourceGUIApp

def main():
    """Main entry point for the application"""
    try:
        # Create main window
        root = tk.Tk()
        
        # Set application icon and basic properties
        root.title("Gource GUI")
        root.geometry("900x700")
        root.minsize(800, 600)
        
        # Center window on screen
        root.update_idletasks()
        x = (root.winfo_screenwidth() // 2) - (900 // 2)
        y = (root.winfo_screenheight() // 2) - (700 // 2)
        root.geometry(f"900x700+{x}+{y}")
        
        # Create and run application
        app = GourceGUIApp(root)
        root.mainloop()
        
    except Exception as e:
        error_msg = f"Failed to start Gource GUI:\n\n{str(e)}\n\nError details:\n{traceback.format_exc()}"
        try:
            messagebox.showerror("Startup Error", error_msg)
        except:
            print(error_msg, file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
