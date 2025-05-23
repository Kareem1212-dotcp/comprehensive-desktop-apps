"""
Status Bar Component
Shows current status and file information
"""

import tkinter as tk
from tkinter import ttk

class StatusBar(ttk.Frame):
    def __init__(self, parent, file_manager):
        super().__init__(parent)
        self.file_manager = file_manager
        self.create_statusbar()
        
    def create_statusbar(self):
        """Create status bar with multiple sections"""
        # Status message
        self.status_var = tk.StringVar(value="Ready")
        self.status_label = ttk.Label(self, textvariable=self.status_var)
        self.status_label.pack(side=tk.LEFT, padx=5)
        
        # Separator
        ttk.Separator(self, orient='vertical').pack(side=tk.LEFT, fill='y', padx=5)
        
        # File count
        self.count_var = tk.StringVar(value="0 items")
        self.count_label = ttk.Label(self, textvariable=self.count_var)
        self.count_label.pack(side=tk.LEFT, padx=5)
        
        # Separator
        ttk.Separator(self, orient='vertical').pack(side=tk.LEFT, fill='y', padx=5)
        
        # Current path
        self.path_var = tk.StringVar(value="")
        self.path_label = ttk.Label(self, textvariable=self.path_var)
        self.path_label.pack(side=tk.LEFT, padx=5)
        
        # Selection info (right side)
        self.selection_var = tk.StringVar(value="")
        self.selection_label = ttk.Label(self, textvariable=self.selection_var)
        self.selection_label.pack(side=tk.RIGHT, padx=5)
        
    def update_status(self, message):
        """Update status message"""
        self.status_var.set(message)
        
    def update_path(self, path):
        """Update current path display"""
        self.path_var.set(str(path))
        
    def update_file_count(self, count):
        """Update file count display"""
        if count == 1:
            self.count_var.set("1 item")
        else:
            self.count_var.set(f"{count} items")
            
    def update_selection(self, selected_count, total_size=None):
        """Update selection information"""
        if selected_count == 0:
            self.selection_var.set("")
        elif selected_count == 1:
            if total_size:
                self.selection_var.set(f"1 item selected ({total_size})")
            else:
                self.selection_var.set("1 item selected")
        else:
            if total_size:
                self.selection_var.set(f"{selected_count} items selected ({total_size})")
            else:
                self.selection_var.set(f"{selected_count} items selected")