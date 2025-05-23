"""
Search Dialog
Advanced file search functionality
"""

import tkinter as tk
from tkinter import ttk
import threading
from pathlib import Path
import fnmatch
import re

class SearchDialog:
    def __init__(self, parent, search_path, file_manager):
        self.search_path = search_path
        self.file_manager = file_manager
        self.search_thread = None
        self.results = []
        
        self.dialog = tk.Toplevel(parent)
        self.setup_dialog()
        
    def setup_dialog(self):
        """Setup search dialog"""
        self.dialog.title("Advanced Search")
        self.dialog.geometry("600x500")
        
        # Search criteria frame
        criteria_frame = ttk.LabelFrame(self.dialog, text="Search Criteria", padding=10)
        criteria_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # Filename pattern
        ttk.Label(criteria_frame, text="File name:").grid(row=0, column=0, sticky='w', pady=2)
        self.name_var = tk.StringVar()
        ttk.Entry(criteria_frame, textvariable=self.name_var, width=40).grid(row=0, column=1, sticky='ew', padx=5)
        
        # Content search
        ttk.Label(criteria_frame, text="Content contains:").grid(row=1, column=0, sticky='w', pady=2)
        self.content_var = tk.StringVar()
        ttk.Entry(criteria_frame, textvariable=self.content_var, width=40).grid(row=1, column=1, sticky='ew', padx=5)
        
        # Size criteria
        ttk.Label(criteria_frame, text="Size:").grid(row=2, column=0, sticky='w', pady=2)
        size_frame = ttk.Frame(criteria_frame)
        size_frame.grid(row=2, column=1, sticky='ew', padx=5)
        
        self.size_op_var = tk.StringVar(value="any")
        ttk.Combobox(size_frame, textvariable=self.size_op_var, 
                    values=["any", "greater than", "less than", "equal to"], width=12).pack(side=tk.LEFT)
        
        self.size_var = tk.StringVar()
        ttk.Entry(size_frame, textvariable=self.size_var, width=10).pack(side=tk.LEFT, padx=5)
        
        self.size_unit_var = tk.StringVar(value="KB")
        ttk.Combobox(size_frame, textvariable=self.size_unit_var, 
                    values=["B", "KB", "MB", "GB"], width=6).pack(side=tk.LEFT)
        
        # Options
        options_frame = ttk.LabelFrame(self.dialog, text="Options", padding=10)
        options_frame.pack(fill=tk.X, padx=10, pady=5)
        
        self.case_sensitive_var = tk.BooleanVar()
        ttk.Checkbutton(options_frame, text="Case sensitive", 
                       variable=self.case_sensitive_var).pack(anchor='w')
        
        self.regex_var = tk.BooleanVar()
        ttk.Checkbutton(options_frame, text="Use regular expressions", 
                       variable=self.regex_var).pack(anchor='w')
        
        self.include_subdirs_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(options_frame, text="Include subdirectories", 
                       variable=self.include_subdirs_var).pack(anchor='w')
        
        # Results frame
        results_frame = ttk.LabelFrame(self.dialog, text="Search Results", padding=10)
        results_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Results tree
        self.results_tree = ttk.Treeview(results_frame, columns=('path', 'size', 'modified'))
        self.results_tree.heading('#0', text='Name')
        self.results_tree.heading('path', text='Path')
        self.results_tree.heading('size', text='Size')
        self.results_tree.heading('modified', text='Modified')
        
        # Scrollbars
        v_scroll = ttk.Scrollbar(results_frame, orient='vertical', command=self.results_tree.yview)
        h_scroll = ttk.Scrollbar(results_frame, orient='horizontal', command=self.results_tree.xview)
        self.results_tree.configure(yscrollcommand=v_scroll.set, xscrollcommand=h_scroll.set)
        
        self.results_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        v_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        h_scroll.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Status label
        self.status_var = tk.StringVar(value="Ready to search")
        ttk.Label(results_frame, textvariable=self.status_var).pack(fill=tk.X, pady=5)
        
        # Button frame
        button_frame = ttk.Frame(self.dialog)
        button_frame.pack(fill=tk.X, padx=10, pady=5)
        
        self.search_btn = ttk.Button(button_frame, text="Search", command=self.start_search)
        self.search_btn.pack(side=tk.LEFT, padx=5)
        
        self.stop_btn = ttk.Button(button_frame, text="Stop", command=self.stop_search, state='disabled')
        self.stop_btn.pack(side=tk.LEFT, padx=5)
        
        ttk.Button(button_frame, text="Close", command=self.dialog.destroy).pack(side=tk.RIGHT, padx=5)
        
        # Configure grid weights
        criteria_frame.columnconfigure(1, weight=1)
        
    def start_search(self):
        """Start search in background thread"""
        if self.search_thread and self.search_thread.is_alive():
            return
            
        self.search_btn.config(state='disabled')
        self.stop_btn.config(state='normal')
        self.results_tree.delete(*self.results_tree.get_children())
        self.results = []
        
        self.search_thread = threading.Thread(target=self.perform_search)
        self.search_thread.daemon = True
        self.search_thread.start()
        
    def stop_search(self):
        """Stop current search"""
        self.search_btn.config(state='normal')
        self.stop_btn.config(state='disabled')
        self.status_var.set("Search stopped")
        
    def perform_search(self):
        """Perform the actual search"""
        try:
            self.status_var.set("Searching...")
            found_count = 0
            
            # Get search criteria
            name_pattern = self.name_var.get()
            content_pattern = self.content_var.get()
            
            # Search files
            for file_path in self.search_files(self.search_path):
                if self.stop_btn['state'] == 'disabled':  # Check if stopped
                    break
                    
                if self.matches_criteria(file_path, name_pattern, content_pattern):
                    self.add_result(file_path)
                    found_count += 1
                    
            self.dialog.after(0, lambda: self.status_var.set(f"Found {found_count} items"))
            
        except Exception as e:
            self.dialog.after(0, lambda: self.status_var.set(f"Search error: {e}"))
        finally:
            self.dialog.after(0, lambda: self.search_btn.config(state='normal'))
            self.dialog.after(0, lambda: self.stop_btn.config(state='disabled'))
            
    def search_files(self, path):
        """Generator to search files"""
        try:
            for item in path.iterdir():
                if item.is_file():
                    yield item
                elif item.is_dir() and self.include_subdirs_var.get():
                    yield from self.search_files(item)
        except PermissionError:
            pass
            
    def matches_criteria(self, file_path, name_pattern, content_pattern):
        """Check if file matches search criteria"""
        # Check filename pattern
        if name_pattern:
            if self.regex_var.get():
                flags = 0 if self.case_sensitive_var.get() else re.IGNORECASE
                if not re.search(name_pattern, file_path.name, flags):
                    return False
            else:
                pattern = name_pattern if self.case_sensitive_var.get() else name_pattern.lower()
                filename = file_path.name if self.case_sensitive_var.get() else file_path.name.lower()
                if not fnmatch.fnmatch(filename, pattern):
                    return False
                    
        # Check content pattern
        if content_pattern and file_path.is_file():
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    if self.case_sensitive_var.get():
                        if content_pattern not in content:
                            return False
                    else:
                        if content_pattern.lower() not in content.lower():
                            return False
            except:
                return False
                
        # Check size criteria
        if self.size_op_var.get() != "any" and self.size_var.get():
            try:
                size_value = float(self.size_var.get())
                unit = self.size_unit_var.get()
                multiplier = {'B': 1, 'KB': 1024, 'MB': 1024**2, 'GB': 1024**3}[unit]
                target_size = size_value * multiplier
                
                file_size = file_path.stat().st_size
                op = self.size_op_var.get()
                
                if op == "greater than" and file_size <= target_size:
                    return False
                elif op == "less than" and file_size >= target_size:
                    return False
                elif op == "equal to" and abs(file_size - target_size) > 1024:
                    return False
            except:
                pass
                
        return True
        
    def add_result(self, file_path):
        """Add search result to tree"""
        try:
            stat = file_path.stat()
            size = self.format_size(stat.st_size) if file_path.is_file() else ""
            from datetime import datetime
            modified = datetime.fromtimestamp(stat.st_mtime).strftime('%Y-%m-%d %H:%M')
            
            self.dialog.after(0, lambda: self.results_tree.insert('', 'end', 
                text=file_path.name,
                values=(str(file_path.parent), size, modified)))
        except:
            pass
            
    def format_size(self, size):
        """Format file size"""
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size < 1024.0:
                return f"{size:.1f} {unit}"
            size /= 1024.0
        return f"{size:.1f} TB"