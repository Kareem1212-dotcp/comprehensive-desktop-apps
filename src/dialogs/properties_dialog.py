"""
Properties Dialog
Shows detailed file/folder properties
"""

import tkinter as tk
from tkinter import ttk
from pathlib import Path
from datetime import datetime
import os
import stat

class PropertiesDialog:
    def __init__(self, parent, file_path):
        self.file_path = Path(file_path)
        self.dialog = tk.Toplevel(parent)
        self.setup_dialog()
        
    def setup_dialog(self):
        """Setup the properties dialog"""
        self.dialog.title(f"Properties - {self.file_path.name}")
        self.dialog.geometry("400x500")
        self.dialog.resizable(False, False)
        
        # Center dialog
        self.dialog.transient()
        self.dialog.grab_set()
        
        # Create notebook for tabs
        notebook = ttk.Notebook(self.dialog)
        notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # General tab
        self.create_general_tab(notebook)
        
        # Security tab
        self.create_security_tab(notebook)
        
        # Button frame
        button_frame = ttk.Frame(self.dialog)
        button_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Button(button_frame, text="OK", command=self.dialog.destroy).pack(side=tk.RIGHT, padx=5)
        
    def create_general_tab(self, notebook):
        """Create general properties tab"""
        general_frame = ttk.Frame(notebook)
        notebook.add(general_frame, text="General")
        
        # File icon and name
        header_frame = ttk.Frame(general_frame)
        header_frame.pack(fill=tk.X, padx=10, pady=10)
        
        icon_label = ttk.Label(header_frame, text="📁" if self.file_path.is_dir() else "📄", font=("Arial", 24))
        icon_label.pack(side=tk.LEFT, padx=10)
        
        name_label = ttk.Label(header_frame, text=self.file_path.name, font=("Arial", 12, "bold"))
        name_label.pack(side=tk.LEFT, anchor='w')
        
        # Properties
        props_frame = ttk.LabelFrame(general_frame, text="Properties", padding=10)
        props_frame.pack(fill=tk.X, padx=10, pady=5)
        
        try:
            file_stat = self.file_path.stat()
            
            # Type
            file_type = "Folder" if self.file_path.is_dir() else self.get_file_type()
            self.add_property(props_frame, "Type:", file_type, 0)
            
            # Location
            self.add_property(props_frame, "Location:", str(self.file_path.parent), 1)
            
            # Size
            if self.file_path.is_file():
                size = self.format_size(file_stat.st_size)
                self.add_property(props_frame, "Size:", f"{size} ({file_stat.st_size:,} bytes)", 2)
            else:
                self.add_property(props_frame, "Size:", "Calculating...", 2)
                
            # Dates
            created = datetime.fromtimestamp(file_stat.st_ctime).strftime('%Y-%m-%d %H:%M:%S')
            modified = datetime.fromtimestamp(file_stat.st_mtime).strftime('%Y-%m-%d %H:%M:%S')
            accessed = datetime.fromtimestamp(file_stat.st_atime).strftime('%Y-%m-%d %H:%M:%S')
            
            self.add_property(props_frame, "Created:", created, 3)
            self.add_property(props_frame, "Modified:", modified, 4)
            self.add_property(props_frame, "Accessed:", accessed, 5)
            
        except Exception as e:
            self.add_property(props_frame, "Error:", str(e), 0)
            
    def create_security_tab(self, notebook):
        """Create security/permissions tab"""
        security_frame = ttk.Frame(notebook)
        notebook.add(security_frame, text="Security")
        
        perms_frame = ttk.LabelFrame(security_frame, text="Permissions", padding=10)
        perms_frame.pack(fill=tk.X, padx=10, pady=10)
        
        try:
            file_stat = self.file_path.stat()
            mode = file_stat.st_mode
            
            # Owner permissions
            owner_frame = ttk.LabelFrame(perms_frame, text="Owner", padding=5)
            owner_frame.pack(fill=tk.X, pady=5)
            
            ttk.Checkbutton(owner_frame, text="Read", 
                           state='normal' if mode & stat.S_IRUSR else 'disabled').pack(anchor='w')
            ttk.Checkbutton(owner_frame, text="Write", 
                           state='normal' if mode & stat.S_IWUSR else 'disabled').pack(anchor='w')
            ttk.Checkbutton(owner_frame, text="Execute", 
                           state='normal' if mode & stat.S_IXUSR else 'disabled').pack(anchor='w')
            
            # Group permissions
            group_frame = ttk.LabelFrame(perms_frame, text="Group", padding=5)
            group_frame.pack(fill=tk.X, pady=5)
            
            ttk.Checkbutton(group_frame, text="Read", 
                           state='normal' if mode & stat.S_IRGRP else 'disabled').pack(anchor='w')
            ttk.Checkbutton(group_frame, text="Write", 
                           state='normal' if mode & stat.S_IWGRP else 'disabled').pack(anchor='w')
            ttk.Checkbutton(group_frame, text="Execute", 
                           state='normal' if mode & stat.S_IXGRP else 'disabled').pack(anchor='w')
            
            # Other permissions
            other_frame = ttk.LabelFrame(perms_frame, text="Others", padding=5)
            other_frame.pack(fill=tk.X, pady=5)
            
            ttk.Checkbutton(other_frame, text="Read", 
                           state='normal' if mode & stat.S_IROTH else 'disabled').pack(anchor='w')
            ttk.Checkbutton(other_frame, text="Write", 
                           state='normal' if mode & stat.S_IWOTH else 'disabled').pack(anchor='w')
            ttk.Checkbutton(other_frame, text="Execute", 
                           state='normal' if mode & stat.S_IXOTH else 'disabled').pack(anchor='w')
            
        except Exception as e:
            ttk.Label(perms_frame, text=f"Error reading permissions: {e}").pack()
            
    def add_property(self, parent, label, value, row):
        """Add a property row"""
        ttk.Label(parent, text=label, font=("Arial", 9, "bold")).grid(row=row, column=0, sticky='w', padx=5, pady=2)
        ttk.Label(parent, text=value, font=("Arial", 9)).grid(row=row, column=1, sticky='w', padx=10, pady=2)
        
    def get_file_type(self):
        """Get file type description"""
        import mimetypes
        mime_type, _ = mimetypes.guess_type(str(self.file_path))
        if mime_type:
            return mime_type
        else:
            ext = self.file_path.suffix.lower()
            return f"{ext[1:].upper()} File" if ext else "File"
            
    def format_size(self, size):
        """Format file size"""
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if size < 1024.0:
                return f"{size:.1f} {unit}"
            size /= 1024.0
        return f"{size:.1f} PB"