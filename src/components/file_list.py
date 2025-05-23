"""
File List Component
Displays files and folders in the main view
"""

import tkinter as tk
from tkinter import ttk
import os
from pathlib import Path
from datetime import datetime
import mimetypes

class FileListView(ttk.Treeview):
    def __init__(self, parent, file_manager):
        super().__init__(parent, show='tree headings')
        self.file_manager = file_manager
        self.view_mode = 'detail'
        self.setup_columns()
        self.setup_bindings()
        
    def setup_columns(self):
        """Setup columns for file list"""
        self['columns'] = ('size', 'type', 'modified')
        
        # Configure columns
        self.heading('#0', text='Name', anchor='w')
        self.heading('size', text='Size', anchor='e')
        self.heading('type', text='Type', anchor='w')
        self.heading('modified', text='Modified', anchor='w')
        
        self.column('#0', width=300, minwidth=200)
        self.column('size', width=80, minwidth=60)
        self.column('type', width=100, minwidth=80)
        self.column('modified', width=150, minwidth=120)
        
        # Add scrollbars
        v_scrollbar = ttk.Scrollbar(self.master, orient='vertical', command=self.yview)
        v_scrollbar.pack(side='right', fill='y')
        self.configure(yscrollcommand=v_scrollbar.set)
        
        h_scrollbar = ttk.Scrollbar(self.master, orient='horizontal', command=self.xview)
        h_scrollbar.pack(side='bottom', fill='x')
        self.configure(xscrollcommand=h_scrollbar.set)
        
    def setup_bindings(self):
        """Setup event bindings"""
        self.bind('<Double-1>', self.on_double_click)
        self.bind('<Button-3>', self.on_right_click)
        self.bind('<<TreeviewSelect>>', self.on_select)
        
    def update_list(self, path):
        """Update file list for given path"""
        # Clear existing items
        self.delete(*self.get_children())
        
        try:
            items = []
            
            # Add parent directory link
            if path.parent != path:
                items.append({
                    'name': '..',
                    'path': path.parent,
                    'is_dir': True,
                    'size': '',
                    'type': 'Folder',
                    'modified': ''
                })
            
            # Get directory contents
            for item in sorted(path.iterdir(), key=lambda x: (not x.is_dir(), x.name.lower())):
                if item.name.startswith('.') and not self.file_manager.settings.get('show_hidden', False):
                    continue
                    
                item_info = self.get_item_info(item)
                items.append(item_info)
                
            # Add items to tree
            for item in items:
                icon = self.get_icon(item)
                self.insert('', 'end',
                           text=f"{icon} {item['name']}",
                           values=(item['size'], item['type'], item['modified']),
                           tags=('directory' if item['is_dir'] else 'file',))
                           
        except PermissionError:
            self.insert('', 'end', text="❌ Permission Denied", values=('', '', ''))
        except Exception as e:
            self.insert('', 'end', text=f"❌ Error: {str(e)}", values=('', '', ''))
            
    def get_item_info(self, path):
        """Get information about a file/directory"""
        try:
            stat = path.stat()
            
            if path.is_dir():
                size = ''
                file_type = 'Folder'
            else:
                size = self.format_size(stat.st_size)
                file_type = self.get_file_type(path)
                
            modified = datetime.fromtimestamp(stat.st_mtime).strftime('%Y-%m-%d %H:%M')
            
            return {
                'name': path.name,
                'path': path,
                'is_dir': path.is_dir(),
                'size': size,
                'type': file_type,
                'modified': modified
            }
        except:
            return {
                'name': path.name,
                'path': path,
                'is_dir': path.is_dir(),
                'size': '',
                'type': 'Unknown',
                'modified': ''
            }
            
    def format_size(self, size):
        """Format file size in human readable format"""
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if size < 1024.0:
                return f"{size:.1f} {unit}"
            size /= 1024.0
        return f"{size:.1f} PB"
        
    def get_file_type(self, path):
        """Get file type description"""
        mime_type, _ = mimetypes.guess_type(str(path))
        if mime_type:
            if mime_type.startswith('image/'):
                return 'Image'
            elif mime_type.startswith('video/'):
                return 'Video'
            elif mime_type.startswith('audio/'):
                return 'Audio'
            elif mime_type.startswith('text/'):
                return 'Text'
            elif 'pdf' in mime_type:
                return 'PDF'
            elif 'zip' in mime_type or 'archive' in mime_type:
                return 'Archive'
                
        ext = path.suffix.lower()
        if ext in ['.py', '.js', '.html', '.css', '.cpp', '.java']:
            return 'Code'
        elif ext in ['.doc', '.docx', '.odt']:
            return 'Document'
        elif ext in ['.xls', '.xlsx', '.csv']:
            return 'Spreadsheet'
        elif ext in ['.ppt', '.pptx']:
            return 'Presentation'
        else:
            return 'File'
            
    def get_icon(self, item):
        """Get icon for file/directory"""
        if item['is_dir']:
            if item['name'] == '..':
                return '⬆️'
            return '📁'
        else:
            file_type = item['type']
            icons = {
                'Image': '🖼️',
                'Video': '🎬',
                'Audio': '🎵',
                'Text': '📝',
                'PDF': '📄',
                'Archive': '🗜️',
                'Code': '💻',
                'Document': '📄',
                'Spreadsheet': '📊',
                'Presentation': '📽️'
            }
            return icons.get(file_type, '📄')
            
    def on_double_click(self, event):
        """Handle double-click"""
        selection = self.selection()
        if selection:
            item = selection[0]
            text = self.item(item, 'text')
            name = text.split(' ', 1)[1] if ' ' in text else text
            self.file_manager.open_selected()
            
    def on_right_click(self, event):
        """Handle right-click context menu"""
        # Create context menu
        context_menu = tk.Menu(self, tearoff=0)
        context_menu.add_command(label="Open", command=self.file_manager.open_selected)
        context_menu.add_command(label="Open with...", command=self.file_manager.open_with)
        context_menu.add_separator()
        context_menu.add_command(label="Cut", command=self.file_manager.cut_files)
        context_menu.add_command(label="Copy", command=self.file_manager.copy_files)
        context_menu.add_command(label="Paste", command=self.file_manager.paste_files)
        context_menu.add_separator()
        context_menu.add_command(label="Delete", command=self.file_manager.delete_files)
        context_menu.add_command(label="Rename", command=self.file_manager.rename_file)
        context_menu.add_separator()
        context_menu.add_command(label="Properties", command=self.file_manager.show_properties)
        
        try:
            context_menu.tk_popup(event.x_root, event.y_root)
        finally:
            context_menu.grab_release()
            
    def on_select(self, event):
        """Handle selection change"""
        selection = self.get_selection()
        if selection:
            path = self.file_manager.current_path / selection[0].split(' ', 1)[1]
            if path.exists() and path.is_file():
                self.file_manager.preview_panel.update_preview(path)
                
    def get_selection(self):
        """Get selected items"""
        selection = self.selection()
        items = []
        for item in selection:
            text = self.item(item, 'text')
            name = text.split(' ', 1)[1] if ' ' in text else text
            if name != '..':
                items.append(name)
        return items
        
    def select_all(self):
        """Select all items"""
        self.selection_set(self.get_children())
        
    def set_view_mode(self, mode):
        """Set view mode"""
        self.view_mode = mode
        # Implementation for different view modes
        pass