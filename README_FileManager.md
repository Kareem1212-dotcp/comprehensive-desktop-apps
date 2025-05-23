# Advanced File Manager Desktop Application

A comprehensive, feature-rich file management solution built with Python and Tkinter.

## 🚀 Features

### Core File Management
- **Dual-Pane Interface**: Directory tree and file list with resizable panels
- **File Operations**: Copy, move, delete, rename with progress tracking
- **Advanced Search**: Content search, regex support, size filters
- **File Preview**: Text files, images, and directory contents
- **Clipboard Integration**: Cut, copy, paste operations

### User Interface
- **Multiple Themes**: Default, Dark, Blue, Green color schemes
- **Customizable Views**: List, Icon, Detail view modes
- **Resizable Panels**: Adjustable sidebar and preview panel
- **Status Bar**: Real-time feedback and file information
- **Toolbar**: Quick access to common operations

### Advanced Features
- **Properties Dialog**: Detailed file information and permissions
- **Preferences**: Extensive customization options
- **File Associations**: Custom application mappings
- **Duplicate Finder**: Locate duplicate files by content hash
- **Folder Size Calculator**: Calculate directory sizes
- **Archive Support**: Create and extract zip files

### Navigation
- **Breadcrumb Navigation**: Address bar with path editing
- **Bookmarks**: Save favorite locations
- **Recent Locations**: Quick access to recently visited folders
- **Keyboard Shortcuts**: Comprehensive hotkey support

### Technical Features
- **Multi-threading**: Background operations don't block UI
- **Logging System**: Comprehensive error tracking
- **Settings Persistence**: Automatic configuration saving
- **Cross-platform**: Works on Windows, macOS, and Linux

## 🎯 Installation

### Requirements
- Python 3.7 or higher
- No additional dependencies (uses only Python standard library)

### Running the Application
```bash
python main.py
```

## ⌨️ Keyboard Shortcuts

### File Operations
- `Ctrl+N` - New Folder
- `Ctrl+Shift+N` - New File
- `Enter` - Open selected item
- `Alt+Enter` - Properties
- `F2` - Rename
- `Delete` - Delete selected items

### Edit Operations
- `Ctrl+X` - Cut
- `Ctrl+C` - Copy
- `Ctrl+V` - Paste
- `Ctrl+A` - Select All

### Navigation
- `F5` - Refresh
- `Backspace` - Go to parent directory
- `Ctrl+F` - Search
- `Ctrl+,` - Preferences

## 🎨 Themes

Choose from multiple color themes:
- **Default**: Classic light theme
- **Dark**: Modern dark theme for low-light environments
- **Blue**: Professional blue color scheme
- **Green**: Nature-inspired green theme

## 📁 File Structure

```
Advanced File Manager/
├── main.py                     # Application entry point
├── src/
│   ├── file_manager.py         # Main window and core logic
│   ├── settings_manager.py     # Configuration management
│   ├── theme_manager.py        # Theme and styling
│   ├── components/             # UI Components
│   │   ├── file_tree.py        # Directory tree view
│   │   ├── file_list.py        # File listing component
│   │   ├── preview_panel.py    # File preview panel
│   │   ├── toolbar.py          # Navigation toolbar
│   │   └── statusbar.py        # Status information bar
│   ├── dialogs/                # Dialog windows
│   │   ├── properties_dialog.py # File properties
│   │   ├── search_dialog.py    # Advanced search
│   │   └── preferences_dialog.py # Settings
│   └── utils/                  # Utility modules
│       ├── logger.py           # Logging system
│       └── file_operations.py  # File manipulation
├── config/                     # Configuration files
├── data/                       # Application data
├── assets/                     # Icons and themes
└── logs/                       # Log files
```

## 🔧 Configuration

Settings are automatically saved in `config/settings.json` and include:
- Theme preferences
- View modes
- Panel visibility
- File associations
- Recent locations
- Bookmarks

## 🚀 Advanced Usage

### Custom File Associations
Associate file types with specific applications through the Preferences dialog.

### Search Features
- **Filename patterns**: Use wildcards (*) or regex
- **Content search**: Search inside text files
- **Size filters**: Find files by size criteria
- **Advanced options**: Case sensitivity, subdirectory inclusion

### Themes and Customization
- Switch themes instantly from Preferences
- Customize panel layouts
- Configure toolbar visibility
- Set default view modes

## 🤝 Contributing

This is a comprehensive desktop file manager with extensive features for power users and developers.

## 📄 License

Open source desktop application built with Python.

---

**Enjoy managing your files with style and efficiency!** 🎉