"""
Preferences Dialog
Application settings and configuration
"""

import tkinter as tk
from tkinter import ttk

class PreferencesDialog:
    def __init__(self, parent, settings, theme_manager):
        self.settings = settings
        self.theme_manager = theme_manager
        self.dialog = tk.Toplevel(parent)
        self.setup_dialog()
        
    def setup_dialog(self):
        """Setup preferences dialog"""
        self.dialog.title("Preferences")
        self.dialog.geometry("500x400")
        self.dialog.resizable(False, False)
        
        # Create notebook
        notebook = ttk.Notebook(self.dialog)
        notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # General tab
        self.create_general_tab(notebook)
        
        # Appearance tab
        self.create_appearance_tab(notebook)
        
        # Advanced tab
        self.create_advanced_tab(notebook)
        
        # Button frame
        button_frame = ttk.Frame(self.dialog)
        button_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Button(button_frame, text="OK", command=self.save_and_close).pack(side=tk.RIGHT, padx=5)
        ttk.Button(button_frame, text="Cancel", command=self.dialog.destroy).pack(side=tk.RIGHT, padx=5)
        ttk.Button(button_frame, text="Apply", command=self.apply_settings).pack(side=tk.RIGHT, padx=5)
        
    def create_general_tab(self, notebook):
        """Create general preferences tab"""
        general_frame = ttk.Frame(notebook)
        notebook.add(general_frame, text="General")
        
        # File operations
        file_ops_frame = ttk.LabelFrame(general_frame, text="File Operations", padding=10)
        file_ops_frame.pack(fill=tk.X, padx=10, pady=5)
        
        self.confirm_delete_var = tk.BooleanVar(value=self.settings.get('confirm_delete', True))
        ttk.Checkbutton(file_ops_frame, text="Confirm file deletions", 
                       variable=self.confirm_delete_var).pack(anchor='w')
        
        self.auto_save_var = tk.BooleanVar(value=self.settings.get('auto_save', True))
        ttk.Checkbutton(file_ops_frame, text="Auto-save settings", 
                       variable=self.auto_save_var).pack(anchor='w')
        
        # Display options
        display_frame = ttk.LabelFrame(general_frame, text="Display", padding=10)
        display_frame.pack(fill=tk.X, padx=10, pady=5)
        
        self.show_hidden_var = tk.BooleanVar(value=self.settings.get('show_hidden', False))
        ttk.Checkbutton(display_frame, text="Show hidden files", 
                       variable=self.show_hidden_var).pack(anchor='w')
        
        self.show_extensions_var = tk.BooleanVar(value=self.settings.get('show_file_extensions', True))
        ttk.Checkbutton(display_frame, text="Show file extensions", 
                       variable=self.show_extensions_var).pack(anchor='w')
        
        # Date format
        date_frame = ttk.Frame(display_frame)
        date_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(date_frame, text="Date format:").pack(side=tk.LEFT)
        self.date_format_var = tk.StringVar(value=self.settings.get('date_format', '%Y-%m-%d %H:%M:%S'))
        date_combo = ttk.Combobox(date_frame, textvariable=self.date_format_var, width=20)
        date_combo['values'] = ('%Y-%m-%d %H:%M:%S', '%d/%m/%Y %H:%M', '%m/%d/%Y %I:%M %p')
        date_combo.pack(side=tk.RIGHT)
        
    def create_appearance_tab(self, notebook):
        """Create appearance preferences tab"""
        appearance_frame = ttk.Frame(notebook)
        notebook.add(appearance_frame, text="Appearance")
        
        # Theme selection
        theme_frame = ttk.LabelFrame(appearance_frame, text="Theme", padding=10)
        theme_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Label(theme_frame, text="Color theme:").pack(anchor='w')
        self.theme_var = tk.StringVar(value=self.theme_manager.get_current_theme())
        theme_combo = ttk.Combobox(theme_frame, textvariable=self.theme_var, 
                                  values=self.theme_manager.get_theme_names(), state='readonly')
        theme_combo.pack(fill=tk.X, pady=5)
        theme_combo.bind('<<ComboboxSelected>>', self.preview_theme)
        
        # View mode
        view_frame = ttk.LabelFrame(appearance_frame, text="Default View", padding=10)
        view_frame.pack(fill=tk.X, padx=10, pady=5)
        
        self.view_mode_var = tk.StringVar(value=self.settings.get('view_mode', 'detail'))
        ttk.Radiobutton(view_frame, text="List view", value='list', 
                       variable=self.view_mode_var).pack(anchor='w')
        ttk.Radiobutton(view_frame, text="Icon view", value='icon', 
                       variable=self.view_mode_var).pack(anchor='w')
        ttk.Radiobutton(view_frame, text="Detail view", value='detail', 
                       variable=self.view_mode_var).pack(anchor='w')
        
        # Panel visibility
        panels_frame = ttk.LabelFrame(appearance_frame, text="Panels", padding=10)
        panels_frame.pack(fill=tk.X, padx=10, pady=5)
        
        self.show_toolbar_var = tk.BooleanVar(value=self.settings.get('toolbar_visible', True))
        ttk.Checkbutton(panels_frame, text="Show toolbar", 
                       variable=self.show_toolbar_var).pack(anchor='w')
        
        self.show_statusbar_var = tk.BooleanVar(value=self.settings.get('statusbar_visible', True))
        ttk.Checkbutton(panels_frame, text="Show status bar", 
                       variable=self.show_statusbar_var).pack(anchor='w')
        
        self.show_preview_var = tk.BooleanVar(value=self.settings.get('show_preview', True))
        ttk.Checkbutton(panels_frame, text="Show preview panel", 
                       variable=self.show_preview_var).pack(anchor='w')
        
    def create_advanced_tab(self, notebook):
        """Create advanced preferences tab"""
        advanced_frame = ttk.Frame(notebook)
        notebook.add(advanced_frame, text="Advanced")
        
        # Performance
        perf_frame = ttk.LabelFrame(advanced_frame, text="Performance", padding=10)
        perf_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Label(perf_frame, text="File preview size limit (MB):").pack(anchor='w')
        self.preview_limit_var = tk.StringVar(value="1")
        ttk.Entry(perf_frame, textvariable=self.preview_limit_var, width=10).pack(anchor='w', pady=2)
        
        # File associations
        assoc_frame = ttk.LabelFrame(advanced_frame, text="File Associations", padding=10)
        assoc_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Association list
        self.assoc_tree = ttk.Treeview(assoc_frame, columns=('application',), height=6)
        self.assoc_tree.heading('#0', text='Extension')
        self.assoc_tree.heading('application', text='Application')
        self.assoc_tree.pack(fill=tk.BOTH, expand=True)
        
        # Association buttons
        assoc_btn_frame = ttk.Frame(assoc_frame)
        assoc_btn_frame.pack(fill=tk.X, pady=5)
        
        ttk.Button(assoc_btn_frame, text="Add", command=self.add_association).pack(side=tk.LEFT, padx=2)
        ttk.Button(assoc_btn_frame, text="Edit", command=self.edit_association).pack(side=tk.LEFT, padx=2)
        ttk.Button(assoc_btn_frame, text="Remove", command=self.remove_association).pack(side=tk.LEFT, padx=2)
        
        # Load current associations
        self.load_associations()
        
    def preview_theme(self, event=None):
        """Preview selected theme"""
        theme_name = self.theme_var.get()
        self.theme_manager.apply_theme(theme_name)
        
    def load_associations(self):
        """Load file associations into tree"""
        associations = self.settings.get('file_associations', {})
        for ext, app in associations.items():
            self.assoc_tree.insert('', 'end', text=ext, values=(app,))
            
    def add_association(self):
        """Add new file association"""
        # Implementation for adding association
        pass
        
    def edit_association(self):
        """Edit selected association"""
        # Implementation for editing association
        pass
        
    def remove_association(self):
        """Remove selected association"""
        selection = self.assoc_tree.selection()
        if selection:
            self.assoc_tree.delete(selection[0])
            
    def apply_settings(self):
        """Apply current settings"""
        self.settings.set('confirm_delete', self.confirm_delete_var.get())
        self.settings.set('auto_save', self.auto_save_var.get())
        self.settings.set('show_hidden', self.show_hidden_var.get())
        self.settings.set('show_file_extensions', self.show_extensions_var.get())
        self.settings.set('date_format', self.date_format_var.get())
        self.settings.set('view_mode', self.view_mode_var.get())
        self.settings.set('toolbar_visible', self.show_toolbar_var.get())
        self.settings.set('statusbar_visible', self.show_statusbar_var.get())
        self.settings.set('show_preview', self.show_preview_var.get())
        
        # Apply theme
        self.theme_manager.apply_theme(self.theme_var.get())
        
    def save_and_close(self):
        """Save settings and close dialog"""
        self.apply_settings()
        self.dialog.destroy()