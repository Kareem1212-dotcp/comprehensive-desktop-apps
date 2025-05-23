"""
Preview Panel Component
Shows file previews and information
"""

import tkinter as tk
from tkinter import ttk, scrolledtext
from pathlib import Path
import mimetypes

class PreviewPanel(ttk.Frame):
    def __init__(self, parent, file_manager):
        super().__init__(parent)
        self.file_manager = file_manager
        self.current_file = None
        self.setup_ui()
        
    def setup_ui(self):
        """Setup preview panel UI"""
        # File info frame
        self.info_frame = ttk.LabelFrame(self, text="File Information", padding=10)
        self.info_frame.pack(fill=tk.X, padx=5, pady=5)
        
        # Info labels
        self.name_label = ttk.Label(self.info_frame, text="Name: -")
        self.name_label.pack(anchor='w')
        
        self.size_label = ttk.Label(self.info_frame, text="Size: -")
        self.size_label.pack(anchor='w')
        
        self.type_label = ttk.Label(self.info_frame, text="Type: -")
        self.type_label.pack(anchor='w')
        
        self.modified_label = ttk.Label(self.info_frame, text="Modified: -")
        self.modified_label.pack(anchor='w')
        
        # Preview frame
        self.preview_frame = ttk.LabelFrame(self, text="Preview", padding=10)
        self.preview_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Preview content
        self.preview_text = scrolledtext.ScrolledText(
            self.preview_frame, 
            height=10, 
            wrap=tk.WORD,
            state='disabled'
        )
        self.preview_text.pack(fill=tk.BOTH, expand=True)
        
    def update_preview(self, file_path):
        """Update preview for selected file"""
        self.current_file = file_path
        
        if not file_path.exists():
            self.clear_preview()
            return
            
        # Update file info
        self.update_file_info(file_path)
        
        # Update preview content
        if file_path.is_file():
            self.show_file_preview(file_path)
        else:
            self.show_directory_info(file_path)
            
    def update_file_info(self, file_path):
        """Update file information display"""
        try:
            stat = file_path.stat()
            
            self.name_label.config(text=f"Name: {file_path.name}")
            
            if file_path.is_file():
                size = self.format_size(stat.st_size)
                self.size_label.config(text=f"Size: {size}")
            else:
                self.size_label.config(text="Size: -")
                
            file_type = self.get_file_type(file_path)
            self.type_label.config(text=f"Type: {file_type}")
            
            from datetime import datetime
            modified = datetime.fromtimestamp(stat.st_mtime).strftime('%Y-%m-%d %H:%M:%S')
            self.modified_label.config(text=f"Modified: {modified}")
            
        except Exception as e:
            self.name_label.config(text=f"Name: {file_path.name}")
            self.size_label.config(text="Size: -")
            self.type_label.config(text="Type: Unknown")
            self.modified_label.config(text="Modified: -")
            
    def show_file_preview(self, file_path):
        """Show file content preview"""
        self.preview_text.config(state='normal')
        self.preview_text.delete(1.0, tk.END)
        
        try:
            # Check file size
            if file_path.stat().st_size > 1024 * 1024:  # 1MB limit
                self.preview_text.insert(tk.END, "File too large for preview")
            else:
                mime_type, _ = mimetypes.guess_type(str(file_path))
                
                if mime_type and mime_type.startswith('text/'):
                    # Text file preview
                    try:
                        with open(file_path, 'r', encoding='utf-8') as f:
                            content = f.read(10000)  # First 10KB
                            self.preview_text.insert(tk.END, content)
                            if len(content) == 10000:
                                self.preview_text.insert(tk.END, "\n\n... (truncated)")
                    except UnicodeDecodeError:
                        self.preview_text.insert(tk.END, "Binary file - cannot preview")
                        
                elif mime_type and mime_type.startswith('image/'):
                    self.preview_text.insert(tk.END, f"Image file: {file_path.name}\n")
                    self.preview_text.insert(tk.END, f"Type: {mime_type}\n")
                    self.preview_text.insert(tk.END, "Image preview not available in text mode")
                    
                else:
                    # Try to read as text anyway
                    try:
                        with open(file_path, 'r', encoding='utf-8') as f:
                            content = f.read(1000)
                            if content.isprintable():
                                self.preview_text.insert(tk.END, content)
                            else:
                                self.preview_text.insert(tk.END, "Binary file - cannot preview")
                    except:
                        self.preview_text.insert(tk.END, "Cannot preview this file type")
                        
        except Exception as e:
            self.preview_text.insert(tk.END, f"Error reading file: {e}")
            
        self.preview_text.config(state='disabled')
        
    def show_directory_info(self, dir_path):
        """Show directory information"""
        self.preview_text.config(state='normal')
        self.preview_text.delete(1.0, tk.END)
        
        try:
            items = list(dir_path.iterdir())
            folders = [item for item in items if item.is_dir()]
            files = [item for item in items if item.is_file()]
            
            self.preview_text.insert(tk.END, f"Directory: {dir_path.name}\n\n")
            self.preview_text.insert(tk.END, f"Contains:\n")
            self.preview_text.insert(tk.END, f"  📁 {len(folders)} folders\n")
            self.preview_text.insert(tk.END, f"  📄 {len(files)} files\n\n")
            
            if len(items) <= 20:  # Show contents if not too many
                self.preview_text.insert(tk.END, "Contents:\n")
                for item in sorted(items, key=lambda x: (not x.is_dir(), x.name)):
                    icon = "📁" if item.is_dir() else "📄"
                    self.preview_text.insert(tk.END, f"  {icon} {item.name}\n")
            else:
                self.preview_text.insert(tk.END, f"Too many items to list ({len(items)} total)")
                
        except PermissionError:
            self.preview_text.insert(tk.END, "Permission denied")
        except Exception as e:
            self.preview_text.insert(tk.END, f"Error: {e}")
            
        self.preview_text.config(state='disabled')
        
    def clear_preview(self):
        """Clear preview panel"""
        self.name_label.config(text="Name: -")
        self.size_label.config(text="Size: -")
        self.type_label.config(text="Type: -")
        self.modified_label.config(text="Modified: -")
        
        self.preview_text.config(state='normal')
        self.preview_text.delete(1.0, tk.END)
        self.preview_text.config(state='disabled')
        
    def format_size(self, size):
        """Format file size"""
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if size < 1024.0:
                return f"{size:.1f} {unit}"
            size /= 1024.0
        return f"{size:.1f} PB"
        
    def get_file_type(self, path):
        """Get file type description"""
        if path.is_dir():
            return "Folder"
            
        mime_type, _ = mimetypes.guess_type(str(path))
        if mime_type:
            return mime_type
        else:
            ext = path.suffix.lower()
            if ext:
                return f"{ext[1:].upper()} File"
            else:
                return "File"