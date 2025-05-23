#!/usr/bin/env python3
"""
Advanced File Manager Desktop Application
A comprehensive file management solution with modern features
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import os
import sys
from pathlib import Path

# Import custom modules
from src.file_manager import FileManagerWindow
from src.settings_manager import SettingsManager
from src.theme_manager import ThemeManager
from src.utils.logger import Logger

class FileManagerApp:
    def __init__(self):
        self.root = tk.Tk()
        self.setup_application()
        
    def setup_application(self):
        """Initialize the main application"""
        # Initialize managers
        self.settings = SettingsManager()
        self.theme_manager = ThemeManager(self.root)
        self.logger = Logger()
        
        # Apply theme
        self.theme_manager.apply_theme(self.settings.get('theme', 'default'))
        
        # Create main window
        self.file_manager = FileManagerWindow(
            self.root, 
            self.settings, 
            self.theme_manager,
            self.logger
        )
        
        # Setup window properties
        self.root.title("Advanced File Manager")
        self.root.geometry("1200x800")
        self.root.minsize(800, 600)
        
        # Center window
        self.center_window()
        
        # Setup close handler
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
    def center_window(self):
        """Center the main window on screen"""
        self.root.update_idletasks()
        width = 1200
        height = 800
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f"{width}x{height}+{x}+{y}")
        
    def on_closing(self):
        """Handle application closing"""
        try:
            # Save settings
            self.settings.save()
            self.logger.info("Application closed successfully")
        except Exception as e:
            self.logger.error(f"Error during shutdown: {e}")
        finally:
            self.root.destroy()
            
    def run(self):
        """Start the application"""
        self.logger.info("Starting Advanced File Manager")
        self.root.mainloop()

def main():
    """Main entry point"""
    try:
        app = FileManagerApp()
        app.run()
    except Exception as e:
        messagebox.showerror("Error", f"Failed to start application: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()