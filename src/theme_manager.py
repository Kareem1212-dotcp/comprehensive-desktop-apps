"""
Theme Manager Module
Handles application themes and styling
"""

import tkinter as tk
from tkinter import ttk
import json
from pathlib import Path

class ThemeManager:
    def __init__(self, root):
        self.root = root
        self.current_theme = 'default'
        self.themes = self.load_themes()
        
    def load_themes(self):
        """Load available themes"""
        return {
            'default': {
                'name': 'Default',
                'bg': '#f0f0f0',
                'fg': '#000000',
                'select_bg': '#0078d4',
                'select_fg': '#ffffff',
                'button_bg': '#e1e1e1',
                'entry_bg': '#ffffff',
                'frame_bg': '#f0f0f0'
            },
            'dark': {
                'name': 'Dark',
                'bg': '#2d2d2d',
                'fg': '#ffffff',
                'select_bg': '#404040',
                'select_fg': '#ffffff',
                'button_bg': '#404040',
                'entry_bg': '#3d3d3d',
                'frame_bg': '#2d2d2d'
            },
            'blue': {
                'name': 'Blue',
                'bg': '#e6f3ff',
                'fg': '#003366',
                'select_bg': '#0066cc',
                'select_fg': '#ffffff',
                'button_bg': '#cce6ff',
                'entry_bg': '#ffffff',
                'frame_bg': '#e6f3ff'
            },
            'green': {
                'name': 'Green',
                'bg': '#f0fff0',
                'fg': '#006600',
                'select_bg': '#228b22',
                'select_fg': '#ffffff',
                'button_bg': '#e6ffe6',
                'entry_bg': '#ffffff',
                'frame_bg': '#f0fff0'
            }
        }
        
    def apply_theme(self, theme_name):
        """Apply a theme to the application"""
        if theme_name not in self.themes:
            theme_name = 'default'
            
        self.current_theme = theme_name
        theme = self.themes[theme_name]
        
        # Configure ttk styles
        style = ttk.Style()
        
        # Configure main styles
        style.configure('TFrame', background=theme['frame_bg'])
        style.configure('TLabel', background=theme['bg'], foreground=theme['fg'])
        style.configure('TButton', background=theme['button_bg'], foreground=theme['fg'])
        style.configure('TEntry', background=theme['entry_bg'], foreground=theme['fg'])
        
        # Configure treeview
        style.configure('Treeview', 
                       background=theme['bg'],
                       foreground=theme['fg'],
                       fieldbackground=theme['bg'])
        style.map('Treeview',
                 background=[('selected', theme['select_bg'])],
                 foreground=[('selected', theme['select_fg'])])
                 
        # Apply to root window
        self.root.configure(bg=theme['bg'])
        
    def get_theme_names(self):
        """Get list of available theme names"""
        return list(self.themes.keys())
        
    def get_current_theme(self):
        """Get current theme name"""
        return self.current_theme