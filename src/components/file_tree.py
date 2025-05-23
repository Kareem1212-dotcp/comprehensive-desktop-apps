"""
File Tree Component
Displays directory structure in a tree view
"""

import tkinter as tk
from tkinter import ttk
import os
from pathlib import Path

class FileTreeView(ttk.Treeview):
    def __init__(self, parent, file_manager):
        super().__init__(parent)
        self.file_manager = file_manager
        self.setup_tree()
        self.bind('<<TreeviewSelect>>', self.on_select)
        self.bind('<Double-1>', self.on_double_click)
        
    def setup_tree(self):
        """Setup the tree view"""
        self.heading('#0', text='Directories', anchor='w')
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(self.master, orient='vertical', command=self.yview)
        scrollbar.pack(side='right', fill='y')
        self.configure(yscrollcommand=scrollbar.set)
        
        # Populate with root directories
        self.populate_roots()
        
    def populate_roots(self):
        """Populate tree with root directories"""
        # Add home directory
        home = Path.home()
        home_id = self.insert('', 'end', text=f'🏠 {home.name}', values=[str(home)])
        self.populate_directory(home_id, home)
        
        # Add desktop if exists
        desktop = home / 'Desktop'
        if desktop.exists():
            desktop_id = self.insert('', 'end', text=f'🖥️ Desktop', values=[str(desktop)])
            self.populate_directory(desktop_id, desktop)
            
        # Add documents if exists
        documents = home / 'Documents'
        if documents.exists():
            docs_id = self.insert('', 'end', text=f'📁 Documents', values=[str(documents)])
            self.populate_directory(docs_id, documents)
            
        # Add downloads if exists
        downloads = home / 'Downloads'
        if downloads.exists():
            dl_id = self.insert('', 'end', text=f'⬇️ Downloads', values=[str(downloads)])
            self.populate_directory(dl_id, downloads)
            
    def populate_directory(self, parent_id, path):
        """Populate a directory node with subdirectories"""
        try:
            for item in sorted(path.iterdir()):
                if item.is_dir() and not item.name.startswith('.'):
                    icon = '📁'
                    item_id = self.insert(parent_id, 'end', text=f'{icon} {item.name}', values=[str(item)])
                    # Add dummy child to make it expandable
                    self.insert(item_id, 'end', text='Loading...')
        except PermissionError:
            pass
            
    def on_select(self, event):
        """Handle tree selection"""
        selection = self.selection()
        if selection:
            item = selection[0]
            values = self.item(item, 'values')
            if values:
                path = Path(values[0])
                if path.exists() and path.is_dir():
                    self.file_manager.navigate_to(path)
                    
    def on_double_click(self, event):
        """Handle double-click to expand/collapse"""
        item = self.selection()[0]
        if self.item(item, 'open'):
            self.item(item, open=False)
        else:
            self.expand_item(item)
            
    def expand_item(self, item):
        """Expand a tree item"""
        values = self.item(item, 'values')
        if values:
            path = Path(values[0])
            # Remove dummy children
            children = self.get_children(item)
            if children and self.item(children[0], 'text') == 'Loading...':
                self.delete(*children)
                self.populate_directory(item, path)
            self.item(item, open=True)
            
    def update_tree(self, current_path):
        """Update tree to reflect current path"""
        # Expand tree to show current path
        pass