"""
Main File Manager Window Module
Handles the primary file browsing interface
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import os
import shutil
import subprocess
import platform
from pathlib import Path
from datetime import datetime
import mimetypes

from .components.file_tree import FileTreeView
from .components.file_list import FileListView
from .components.preview_panel import PreviewPanel
from .components.toolbar import ToolbarFrame
from .components.statusbar import StatusBar
from .dialogs.properties_dialog import PropertiesDialog
from .dialogs.search_dialog import SearchDialog
from .dialogs.preferences_dialog import PreferencesDialog
from .utils.file_operations import FileOperations

class FileManagerWindow:
    def __init__(self, root, settings, theme_manager, logger):
        self.root = root
        self.settings = settings
        self.theme_manager = theme_manager
        self.logger = logger
        self.current_path = Path.home()
        self.clipboard = []
        self.clipboard_operation = None  # 'cut' or 'copy'
        
        self.setup_ui()
        self.setup_bindings()
        self.load_initial_directory()
        
    def setup_ui(self):
        """Create the main UI layout"""
        # Create main container
        self.main_frame = ttk.Frame(self.root)
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Create menu bar
        self.create_menu_bar()
        
        # Create toolbar
        self.toolbar = ToolbarFrame(self.main_frame, self)
        self.toolbar.pack(fill=tk.X, padx=5, pady=5)
        
        # Create main content area
        self.content_frame = ttk.Frame(self.main_frame)
        self.content_frame.pack(fill=tk.BOTH, expand=True, padx=5)
        
        # Create paned window for resizable layout
        self.paned_window = ttk.PanedWindow(self.content_frame, orient=tk.HORIZONTAL)
        self.paned_window.pack(fill=tk.BOTH, expand=True)
        
        # Left panel - Directory tree
        self.tree_frame = ttk.LabelFrame(self.paned_window, text="Folders", padding=5)
        self.file_tree = FileTreeView(self.tree_frame, self)
        self.file_tree.pack(fill=tk.BOTH, expand=True)
        self.paned_window.add(self.tree_frame, weight=1)
        
        # Right panel container
        self.right_panel = ttk.Frame(self.paned_window)
        self.paned_window.add(self.right_panel, weight=3)
        
        # Right panel - File list and preview
        self.right_paned = ttk.PanedWindow(self.right_panel, orient=tk.VERTICAL)
        self.right_paned.pack(fill=tk.BOTH, expand=True)
        
        # File list area
        self.list_frame = ttk.LabelFrame(self.right_paned, text="Files", padding=5)
        self.file_list = FileListView(self.list_frame, self)
        self.file_list.pack(fill=tk.BOTH, expand=True)
        self.right_paned.add(self.list_frame, weight=2)
        
        # Preview panel
        self.preview_frame = ttk.LabelFrame(self.right_paned, text="Preview", padding=5)
        self.preview_panel = PreviewPanel(self.preview_frame, self)
        self.preview_panel.pack(fill=tk.BOTH, expand=True)
        self.right_paned.add(self.preview_frame, weight=1)
        
        # Status bar
        self.status_bar = StatusBar(self.main_frame, self)
        self.status_bar.pack(fill=tk.X, side=tk.BOTTOM)
        
    def create_menu_bar(self):
        """Create the application menu bar"""
        self.menubar = tk.Menu(self.root)
        self.root.config(menu=self.menubar)
        
        # File menu
        file_menu = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="New Folder", command=self.create_new_folder, accelerator="Ctrl+N")
        file_menu.add_command(label="New File", command=self.create_new_file, accelerator="Ctrl+Shift+N")
        file_menu.add_separator()
        file_menu.add_command(label="Open", command=self.open_selected, accelerator="Enter")
        file_menu.add_command(label="Open With...", command=self.open_with)
        file_menu.add_separator()
        file_menu.add_command(label="Properties", command=self.show_properties, accelerator="Alt+Enter")
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit, accelerator="Ctrl+Q")
        
        # Edit menu
        edit_menu = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="Edit", menu=edit_menu)
        edit_menu.add_command(label="Cut", command=self.cut_files, accelerator="Ctrl+X")
        edit_menu.add_command(label="Copy", command=self.copy_files, accelerator="Ctrl+C")
        edit_menu.add_command(label="Paste", command=self.paste_files, accelerator="Ctrl+V")
        edit_menu.add_separator()
        edit_menu.add_command(label="Delete", command=self.delete_files, accelerator="Delete")
        edit_menu.add_command(label="Rename", command=self.rename_file, accelerator="F2")
        edit_menu.add_separator()
        edit_menu.add_command(label="Select All", command=self.select_all, accelerator="Ctrl+A")
        
        # View menu
        view_menu = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="View", menu=view_menu)
        view_menu.add_command(label="Refresh", command=self.refresh_view, accelerator="F5")
        view_menu.add_separator()
        view_menu.add_command(label="Show Hidden Files", command=self.toggle_hidden_files)
        view_menu.add_command(label="Show Preview Panel", command=self.toggle_preview_panel)
        view_menu.add_separator()
        view_menu.add_command(label="List View", command=lambda: self.change_view_mode("list"))
        view_menu.add_command(label="Icon View", command=lambda: self.change_view_mode("icon"))
        view_menu.add_command(label="Detail View", command=lambda: self.change_view_mode("detail"))
        
        # Tools menu
        tools_menu = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="Tools", menu=tools_menu)
        tools_menu.add_command(label="Search", command=self.open_search_dialog, accelerator="Ctrl+F")
        tools_menu.add_command(label="Calculate Folder Size", command=self.calculate_folder_size)
        tools_menu.add_command(label="Find Duplicates", command=self.find_duplicates)
        tools_menu.add_separator()
        tools_menu.add_command(label="Open Terminal Here", command=self.open_terminal)
        tools_menu.add_command(label="Open Command Prompt", command=self.open_command_prompt)
        tools_menu.add_separator()
        tools_menu.add_command(label="Preferences", command=self.open_preferences, accelerator="Ctrl+,")
        
        # Help menu
        help_menu = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="Keyboard Shortcuts", command=self.show_shortcuts)
        help_menu.add_command(label="About", command=self.show_about)
        
    def setup_bindings(self):
        """Setup keyboard shortcuts and event bindings"""
        # Keyboard shortcuts
        self.root.bind('<Control-n>', lambda e: self.create_new_folder())
        self.root.bind('<Control-Shift-N>', lambda e: self.create_new_file())
        self.root.bind('<Control-x>', lambda e: self.cut_files())
        self.root.bind('<Control-c>', lambda e: self.copy_files())
        self.root.bind('<Control-v>', lambda e: self.paste_files())
        self.root.bind('<Control-a>', lambda e: self.select_all())
        self.root.bind('<Control-f>', lambda e: self.open_search_dialog())
        self.root.bind('<Control-comma>', lambda e: self.open_preferences())
        self.root.bind('<F2>', lambda e: self.rename_file())
        self.root.bind('<F5>', lambda e: self.refresh_view())
        self.root.bind('<Delete>', lambda e: self.delete_files())
        self.root.bind('<Return>', lambda e: self.open_selected())
        self.root.bind('<Alt-Return>', lambda e: self.show_properties())
        
    def load_initial_directory(self):
        """Load the initial directory"""
        initial_path = self.settings.get('last_directory', str(Path.home()))
        self.navigate_to(Path(initial_path))
        
    def navigate_to(self, path):
        """Navigate to a specific directory"""
        try:
            if path.exists() and path.is_dir():
                self.current_path = path
                self.file_tree.update_tree(path)
                self.file_list.update_list(path)
                self.status_bar.update_path(path)
                self.settings.set('last_directory', str(path))
                self.logger.info(f"Navigated to: {path}")
            else:
                messagebox.showerror("Error", f"Cannot access directory: {path}")
        except PermissionError:
            messagebox.showerror("Error", f"Permission denied: {path}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to navigate to {path}: {e}")
            
    def go_up(self):
        """Navigate to parent directory"""
        if self.current_path.parent != self.current_path:
            self.navigate_to(self.current_path.parent)
            
    def go_back(self):
        """Go back in navigation history"""
        # Implementation for navigation history
        pass
        
    def go_forward(self):
        """Go forward in navigation history"""
        # Implementation for navigation history
        pass
        
    def refresh_view(self):
        """Refresh the current view"""
        self.file_list.update_list(self.current_path)
        self.status_bar.update_status("Refreshed")
        
    def create_new_folder(self):
        """Create a new folder"""
        name = tk.simpledialog.askstring("New Folder", "Enter folder name:")
        if name:
            try:
                new_path = self.current_path / name
                new_path.mkdir()
                self.refresh_view()
                self.logger.info(f"Created folder: {new_path}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to create folder: {e}")
                
    def create_new_file(self):
        """Create a new file"""
        name = tk.simpledialog.askstring("New File", "Enter file name:")
        if name:
            try:
                new_path = self.current_path / name
                new_path.touch()
                self.refresh_view()
                self.logger.info(f"Created file: {new_path}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to create file: {e}")
                
    def open_selected(self):
        """Open the selected file or folder"""
        selection = self.file_list.get_selection()
        if selection:
            path = self.current_path / selection[0]
            if path.is_dir():
                self.navigate_to(path)
            else:
                self.open_file(path)
                
    def open_file(self, path):
        """Open a file with the default application"""
        try:
            if platform.system() == 'Windows':
                os.startfile(path)
            elif platform.system() == 'Darwin':  # macOS
                subprocess.run(['open', path])
            else:  # Linux
                subprocess.run(['xdg-open', path])
        except Exception as e:
            messagebox.showerror("Error", f"Failed to open file: {e}")
            
    def open_with(self):
        """Open file with a specific application"""
        # Implementation for open with dialog
        pass
        
    def show_properties(self):
        """Show properties dialog for selected items"""
        selection = self.file_list.get_selection()
        if selection:
            path = self.current_path / selection[0]
            dialog = PropertiesDialog(self.root, path)
            
    def cut_files(self):
        """Cut selected files to clipboard"""
        selection = self.file_list.get_selection()
        if selection:
            self.clipboard = [self.current_path / name for name in selection]
            self.clipboard_operation = 'cut'
            self.status_bar.update_status(f"Cut {len(selection)} item(s)")
            
    def copy_files(self):
        """Copy selected files to clipboard"""
        selection = self.file_list.get_selection()
        if selection:
            self.clipboard = [self.current_path / name for name in selection]
            self.clipboard_operation = 'copy'
            self.status_bar.update_status(f"Copied {len(selection)} item(s)")
            
    def paste_files(self):
        """Paste files from clipboard"""
        if not self.clipboard:
            return
            
        try:
            for source_path in self.clipboard:
                dest_path = self.current_path / source_path.name
                
                if self.clipboard_operation == 'copy':
                    if source_path.is_dir():
                        shutil.copytree(source_path, dest_path)
                    else:
                        shutil.copy2(source_path, dest_path)
                elif self.clipboard_operation == 'cut':
                    shutil.move(source_path, dest_path)
                    
            if self.clipboard_operation == 'cut':
                self.clipboard.clear()
                
            self.refresh_view()
            self.status_bar.update_status("Paste completed")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to paste: {e}")
            
    def delete_files(self):
        """Delete selected files"""
        selection = self.file_list.get_selection()
        if not selection:
            return
            
        if messagebox.askyesno("Confirm Delete", 
                              f"Are you sure you want to delete {len(selection)} item(s)?"):
            try:
                for name in selection:
                    path = self.current_path / name
                    if path.is_dir():
                        shutil.rmtree(path)
                    else:
                        path.unlink()
                        
                self.refresh_view()
                self.status_bar.update_status(f"Deleted {len(selection)} item(s)")
                
            except Exception as e:
                messagebox.showerror("Error", f"Failed to delete: {e}")
                
    def rename_file(self):
        """Rename selected file"""
        selection = self.file_list.get_selection()
        if len(selection) == 1:
            old_name = selection[0]
            new_name = tk.simpledialog.askstring("Rename", "Enter new name:", initialvalue=old_name)
            if new_name and new_name != old_name:
                try:
                    old_path = self.current_path / old_name
                    new_path = self.current_path / new_name
                    old_path.rename(new_path)
                    self.refresh_view()
                    self.logger.info(f"Renamed {old_name} to {new_name}")
                except Exception as e:
                    messagebox.showerror("Error", f"Failed to rename: {e}")
                    
    def select_all(self):
        """Select all items in the current view"""
        self.file_list.select_all()
        
    def toggle_hidden_files(self):
        """Toggle display of hidden files"""
        current = self.settings.get('show_hidden', False)
        self.settings.set('show_hidden', not current)
        self.refresh_view()
        
    def toggle_preview_panel(self):
        """Toggle preview panel visibility"""
        # Implementation for toggling preview panel
        pass
        
    def change_view_mode(self, mode):
        """Change the file list view mode"""
        self.file_list.set_view_mode(mode)
        self.settings.set('view_mode', mode)
        
    def open_search_dialog(self):
        """Open the search dialog"""
        dialog = SearchDialog(self.root, self.current_path, self)
        
    def calculate_folder_size(self):
        """Calculate and display folder sizes"""
        # Implementation for folder size calculation
        pass
        
    def find_duplicates(self):
        """Find duplicate files in the current directory"""
        # Implementation for duplicate file finder
        pass
        
    def open_terminal(self):
        """Open terminal in current directory"""
        try:
            if platform.system() == 'Windows':
                subprocess.run(['cmd'], cwd=self.current_path)
            elif platform.system() == 'Darwin':  # macOS
                subprocess.run(['open', '-a', 'Terminal', self.current_path])
            else:  # Linux
                subprocess.run(['gnome-terminal'], cwd=self.current_path)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to open terminal: {e}")
            
    def open_command_prompt(self):
        """Open command prompt in current directory"""
        self.open_terminal()
        
    def open_preferences(self):
        """Open preferences dialog"""
        dialog = PreferencesDialog(self.root, self.settings, self.theme_manager)
        
    def show_shortcuts(self):
        """Show keyboard shortcuts help"""
        shortcuts = """
Keyboard Shortcuts:

File Operations:
Ctrl+N - New Folder
Ctrl+Shift+N - New File
Enter - Open
Alt+Enter - Properties

Edit Operations:
Ctrl+X - Cut
Ctrl+C - Copy
Ctrl+V - Paste
Delete - Delete
F2 - Rename
Ctrl+A - Select All

Navigation:
F5 - Refresh
Backspace - Go Up

Tools:
Ctrl+F - Search
Ctrl+, - Preferences
"""
        messagebox.showinfo("Keyboard Shortcuts", shortcuts)
        
    def show_about(self):
        """Show about dialog"""
        about_text = """
Advanced File Manager v1.0

A comprehensive file management solution with modern features.

Features:
• Dual-pane interface
• File preview
• Advanced search
• Multiple themes
• Keyboard shortcuts
• And much more!

Built with Python and Tkinter
"""
        messagebox.showinfo("About", about_text)