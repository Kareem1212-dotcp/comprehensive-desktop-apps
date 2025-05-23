"""
Settings Manager Module
Handles application settings and configuration
"""

import json
import os
from pathlib import Path
from typing import Any, Dict

class SettingsManager:
    def __init__(self, config_file="config/settings.json"):
        self.config_file = Path(config_file)
        self.settings = {}
        self.default_settings = {
            'theme': 'default',
            'view_mode': 'detail',
            'show_hidden': False,
            'show_preview': True,
            'window_geometry': '1200x800',
            'last_directory': str(Path.home()),
            'auto_save': True,
            'confirm_delete': True,
            'show_file_extensions': True,
            'date_format': '%Y-%m-%d %H:%M:%S',
            'file_associations': {},
            'recent_locations': [],
            'bookmarks': [],
            'toolbar_visible': True,
            'statusbar_visible': True,
            'sidebar_width': 200,
            'preview_panel_height': 200
        }
        self.load()
        
    def load(self):
        """Load settings from file"""
        try:
            # Create config directory if it doesn't exist
            self.config_file.parent.mkdir(parents=True, exist_ok=True)
            
            if self.config_file.exists():
                with open(self.config_file, 'r') as f:
                    loaded_settings = json.load(f)
                    # Merge with defaults
                    self.settings = {**self.default_settings, **loaded_settings}
            else:
                self.settings = self.default_settings.copy()
                self.save()  # Create initial config file
        except Exception as e:
            print(f"Error loading settings: {e}")
            self.settings = self.default_settings.copy()
            
    def save(self):
        """Save settings to file"""
        try:
            self.config_file.parent.mkdir(parents=True, exist_ok=True)
            with open(self.config_file, 'w') as f:
                json.dump(self.settings, f, indent=2)
        except Exception as e:
            print(f"Error saving settings: {e}")
            
    def get(self, key: str, default: Any = None) -> Any:
        """Get a setting value"""
        return self.settings.get(key, default)
        
    def set(self, key: str, value: Any):
        """Set a setting value"""
        self.settings[key] = value
        if self.get('auto_save', True):
            self.save()
            
    def reset_to_defaults(self):
        """Reset all settings to defaults"""
        self.settings = self.default_settings.copy()
        self.save()
        
    def add_recent_location(self, path: str):
        """Add a location to recent locations"""
        recent = self.get('recent_locations', [])
        if path in recent:
            recent.remove(path)
        recent.insert(0, path)
        # Keep only last 10 locations
        recent = recent[:10]
        self.set('recent_locations', recent)
        
    def add_bookmark(self, name: str, path: str):
        """Add a bookmark"""
        bookmarks = self.get('bookmarks', [])
        bookmark = {'name': name, 'path': path}
        if bookmark not in bookmarks:
            bookmarks.append(bookmark)
            self.set('bookmarks', bookmarks)
            
    def remove_bookmark(self, name: str):
        """Remove a bookmark"""
        bookmarks = self.get('bookmarks', [])
        bookmarks = [b for b in bookmarks if b['name'] != name]
        self.set('bookmarks', bookmarks)
        
    def get_file_association(self, extension: str) -> str:
        """Get file association for an extension"""
        associations = self.get('file_associations', {})
        return associations.get(extension.lower(), '')
        
    def set_file_association(self, extension: str, application: str):
        """Set file association for an extension"""
        associations = self.get('file_associations', {})
        associations[extension.lower()] = application
        self.set('file_associations', associations)