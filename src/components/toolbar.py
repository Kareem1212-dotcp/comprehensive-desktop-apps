"""
Toolbar Component
Navigation and action buttons
"""

import tkinter as tk
from tkinter import ttk

class ToolbarFrame(ttk.Frame):
    def __init__(self, parent, file_manager):
        super().__init__(parent)
        self.file_manager = file_manager
        self.create_toolbar()
        
    def create_toolbar(self):
        """Create toolbar with navigation and action buttons"""
        # Navigation buttons
        nav_frame = ttk.Frame(self)
        nav_frame.pack(side=tk.LEFT, padx=5)
        
        self.back_btn = ttk.Button(nav_frame, text="◀ Back", 
                                  command=self.file_manager.go_back, width=8)
        self.back_btn.pack(side=tk.LEFT, padx=2)
        
        self.forward_btn = ttk.Button(nav_frame, text="▶ Forward", 
                                     command=self.file_manager.go_forward, width=8)
        self.forward_btn.pack(side=tk.LEFT, padx=2)
        
        self.up_btn = ttk.Button(nav_frame, text="⬆ Up", 
                                command=self.file_manager.go_up, width=6)
        self.up_btn.pack(side=tk.LEFT, padx=2)
        
        # Address bar
        addr_frame = ttk.Frame(self)
        addr_frame.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=10)
        
        ttk.Label(addr_frame, text="Location:").pack(side=tk.LEFT)
        self.address_var = tk.StringVar()
        self.address_entry = ttk.Entry(addr_frame, textvariable=self.address_var)
        self.address_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        self.address_entry.bind('<Return>', self.navigate_to_address)
        
        # Action buttons
        action_frame = ttk.Frame(self)
        action_frame.pack(side=tk.RIGHT, padx=5)
        
        self.refresh_btn = ttk.Button(action_frame, text="🔄 Refresh", 
                                     command=self.file_manager.refresh_view, width=10)
        self.refresh_btn.pack(side=tk.LEFT, padx=2)
        
        self.search_btn = ttk.Button(action_frame, text="🔍 Search", 
                                    command=self.file_manager.open_search_dialog, width=10)
        self.search_btn.pack(side=tk.LEFT, padx=2)
        
    def navigate_to_address(self, event):
        """Navigate to address bar location"""
        from pathlib import Path
        path = Path(self.address_var.get())
        if path.exists():
            self.file_manager.navigate_to(path)
            
    def update_address(self, path):
        """Update address bar"""
        self.address_var.set(str(path))