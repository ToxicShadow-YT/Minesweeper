#!/usr/bin/env python3
"""
Build GUI Minesweeper Executable
Creates a professional .exe with graphical interface using tkinter
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path


def build_gui_executable():
    """Build the GUI executable."""
    print("🖥️ Building GUI Minesweeper Executable...")
    
    # Clean previous builds
    for dir_name in ['build', 'dist']:
        if os.path.exists(dir_name):
            shutil.rmtree(dir_name)
    
    # Build the executable
    try:
        subprocess.check_call([
            sys.executable, 
            '-m', 
            'PyInstaller', 
            '--onefile',
            '--windowed',  # No console for GUI app
            '--name=MinesweeperAI_GUI',
            'gui_production.py'
        ])
        
        print("✅ GUI executable built successfully!")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Build failed: {e}")
        return False


def create_gui_launcher():
    """Create GUI launcher script."""
    launcher_content = '''@echo off
title Minesweeper AI - GUI Edition
color 0A

echo.
echo ====================================================
echo    MINESWEEPER AI - Graphical Edition
echo ====================================================
echo.
echo Professional Minesweeper with AI Assistant
echo Features:
echo   - Full graphical interface
echo   - Multiple difficulty levels
echo   - Advanced AI with visual hints
echo   - Statistics tracking
echo   - Professional GUI design
echo.
echo Starting GUI game...
echo.

MinesweeperAI_GUI.exe

if errorlevel 1 (
    echo.
    echo An error occurred while running the game.
    echo Check the log files in %%USERPROFILE%%\\.minesweeper_ai\\
)

echo.
echo Thanks for playing Minesweeper AI GUI!
echo.
pause
'''
    
    with open('Play_Minesweeper_GUI.bat', 'w') as f:
        f.write(launcher_content)
    
    print("✅ Created Play_Minesweeper_GUI.bat")


def create_gui_readme():
    """Create README for GUI version."""
    readme_content = '''# Minesweeper AI - Graphical Edition

A professional-grade Minesweeper game with full graphical interface and advanced AI assistant.

## 🚀 Quick Start

### Option 1: Easy Launch (Recommended)
- Double-click `Play_Minesweeper_GUI.bat`

### Option 2: Direct Launch
- Double-click `MinesweeperAI_GUI.exe`

## 🎮 GUI Features

### Professional Interface
- **Full Graphical Interface**: Modern, intuitive GUI design
- **Visual Board**: Click-based gameplay with visual feedback
- **Real-time Updates**: Live mine counter and timer
- **Professional Theme**: Dark theme with color-coded elements

### Game Controls
- **Left Click**: Reveal cell
- **Right Click**: Place/remove flag
- **Menu Buttons**: New game, AI hints, statistics, settings
- **Difficulty Selector**: Choose from 5 difficulty levels

### AI Assistant
- **Visual Hints**: AI suggestions shown in dialog boxes
- **Apply Hints**: One-click application of AI recommendations
- **Probability Analysis**: Risk assessment for uncertain cells
- **Real-time Analysis**: Get AI help anytime during gameplay

### Difficulty Levels
- **Beginner**: 8x8 board, 10 mines
- **Easy**: 10x10 board, 15 mines
- **Medium**: 12x12 board, 25 mines
- **Hard**: 16x16 board, 40 mines
- **Expert**: 20x20 board, 80 mines

## 🎯 How to Play

### Starting the Game
1. Launch the application
2. Select your preferred difficulty
3. Click any cell to start (first click is always safe)

### Gameplay
- **Left-click** cells to reveal them
- **Right-click** cells to flag suspected mines
- **Numbers** show how many mines are adjacent
- **Reveal all non-mine cells** to win

### AI Assistance
- Click **"AI Hints"** button anytime for help
- View certain mines, safe cells, and probability analysis
- Click **"Apply Hints"** to automatically use AI recommendations

### Menu Options
- **New Game**: Start fresh with current difficulty
- **AI Hints**: Get intelligent suggestions
- **Stats**: View your performance statistics
- **Settings**: Configure game options

## 📊 Statistics Tracking

The GUI automatically tracks:
- Games played and won
- Win rate percentage
- Best completion time
- Average completion time
- AI suggestions used

## 🎨 Visual Features

### Color Scheme
- **Dark Theme**: Professional dark interface
- **Color-coded Numbers**: Each number has unique color
- **Visual Feedback**: Clear indication of cell states
- **Flag Icons**: Visual flag markers

### Cell States
- **Unknown**: Dark gray raised buttons
- **Revealed**: Light gray sunken buttons
- **Numbered**: Colored numbers on revealed cells
- **Flagged**: Flag icon on unknown cells
- **Mine**: Bomb icon (shown on game over)

## ⚙️ Settings

Customize your experience:
- **AI Assistant**: Enable/disable AI suggestions
- **Auto-save**: Automatically save statistics

## 🗂️ File Locations

Configuration and statistics are stored in:
```
%USERPROFILE%\\.minesweeper_ai\\
├── config.json      # Game settings
├── stats.json        # Game statistics
└── logs/            # Application logs
```

## 🔧 Technical Specifications

- **Version**: 1.0.0 GUI Edition
- **Platform**: Windows 10/11
- **Interface**: Tkinter GUI (built-in Python)
- **AI Engine**: Advanced constraint satisfaction and probability analysis
- **Dependencies**: None (fully self-contained executable)
- **Size**: ~10 MB

## 🐛 Troubleshooting

### Common Issues
1. **Game won't start**: Check Windows Defender or antivirus
2. **GUI not responsive**: Restart the application
3. **AI not working**: Ensure AI is enabled in settings

### Error Logs
If you encounter issues, check the log files at:
`%USERPROFILE%\\.minesweeper_ai\\logs\\`

## 📝 Legend

- **Left Click**: Reveal cell
- **Right Click**: Flag/unflag cell
- **Numbers**: Adjacent mine count (color-coded)
- **Flags**: Suspected mine locations
- **AI Hints**: Intelligent suggestions

## 🏆 Tips for Success

1. **Start Smart**: Begin with corners or edges
2. **Use AI**: Click AI Hints button when stuck
3. **Flag First**: Mark certain mines before revealing safe cells
4. **Pattern Recognition**: Learn common mine patterns
5. **Probability**: When uncertain, use AI probability analysis

## 🎮 GUI vs Terminal

### GUI Advantages:
- Visual interface with click controls
- Real-time visual feedback
- Professional appearance
- Easy difficulty switching
- Visual AI hints application

### Terminal Advantages:
- Lightweight and fast
- Works on any terminal
- Lower resource usage
- Keyboard-based controls

Choose the version that best fits your preference!

---

**Minesweeper AI - Graphical Edition v1.0**  
*Professional gaming with artificial intelligence and modern GUI*

Built for the ultimate visual Minesweeper experience with intelligent AI assistance.
'''
    
    with open('README_GUI.md', 'w', encoding='utf-8') as f:
        f.write(readme_content)
    
    print("✅ Created README_GUI.md")


def main():
    """Main GUI build process."""
    print("🖥️ Building GUI Minesweeper AI")
    print("=" * 50)
    
    # Check if we're in the right directory
    if not os.path.exists('gui_production.py'):
        print("❌ gui_production.py not found in current directory")
        return
    
    # Create supporting files
    create_gui_launcher()
    create_gui_readme()
    
    # Build executable
    if not build_gui_executable():
        return
    
    # Check if executable was created
    exe_path = Path('dist/MinesweeperAI_GUI.exe')
    if exe_path.exists():
        print(f"\n🎉 GUI BUILD SUCCESSFUL!")
        print(f"Executable: {exe_path.absolute()}")
        
        # Move to current directory for convenience
        shutil.move('dist/MinesweeperAI_GUI.exe', 'MinesweeperAI_GUI.exe')
        shutil.rmtree('dist')
        
        print(f"\n📦 GUI Package Contents:")
        print("  ✅ MinesweeperAI_GUI.exe - Main GUI executable")
        print("  ✅ Play_Minesweeper_GUI.bat - GUI launcher")
        print("  ✅ README_GUI.md - GUI documentation")
        
        file_size = os.path.getsize('MinesweeperAI_GUI.exe') / (1024 * 1024)  # MB
        print(f"\n📊 Executable size: {file_size:.1f} MB")
        
        print(f"\n🚀 Ready for GUI distribution!")
        print(f"Share these files with end users:")
        print(f"  - MinesweeperAI_GUI.exe")
        print(f"  - Play_Minesweeper_GUI.bat")
        print(f"  - README_GUI.md")
        
        print(f"\n✨ GUI Features:")
        print(f"  - Full graphical interface")
        print(f"  - Click-based gameplay")
        print(f"  - Visual AI hints")
        print(f"  - Professional dark theme")
        print(f"  - Real-time statistics")
        print(f"  - Easy difficulty switching")
        
    else:
        print("❌ GUI executable was not created successfully")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️ Build interrupted by user")
    except Exception as e:
        print(f"\n❌ Build failed with error: {e}")
        import traceback
        traceback.print_exc()
    
    input("\nPress Enter to exit...")
