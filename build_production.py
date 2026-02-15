#!/usr/bin/env python3
"""
Build Production-Ready Minesweeper Executable
Creates a professional .exe with all features enabled
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path


def create_icon():
    """Create a simple icon file (placeholder)."""
    # This would normally create a proper .ico file
    # For now, we'll skip icon creation
    pass


def create_production_spec():
    """Create PyInstaller spec file for production build."""
    spec_content = '''
# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['production_minesweeper.py'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=['dataclasses'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='MinesweeperAI_Pro',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    version='1.0.0',
    description='Production Minesweeper with AI Assistant',
    company='AI Games',
    product='Minesweeper AI',
    copyright='Copyright 2024',
)
'''
    
    with open('production.spec', 'w') as f:
        f.write(spec_content)
    
    print("✅ Created production spec file")


def build_production_executable():
    """Build the production executable."""
    print("🔨 Building Production Executable...")
    
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
            '--console',
            '--name=MinesweeperAI_Pro',
            'production_minesweeper.py'
        ])
        
        print("✅ Production executable built successfully!")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Build failed: {e}")
        return False


def create_installer_script():
    """Create professional installer script."""
    installer_content = '''@echo off
title Minesweeper AI - Production Edition
color 0A

echo.
echo ====================================================
echo    MINESWEEPER AI - Production Edition v1.0
echo ====================================================
echo.
echo Professional Minesweeper with AI Assistant
echo Features:
echo   - Multiple difficulty levels
echo   - Advanced AI with logical deduction
echo   - Statistics tracking
echo   - Configuration system
echo   - Error handling and logging
echo.
echo Starting game...
echo.

MinesweeperAI_Pro.exe

if errorlevel 1 (
    echo.
    echo An error occurred while running the game.
    echo Check the log files in %%USERPROFILE%%\\.minesweeper_ai\\
)

echo.
echo Thanks for playing Minesweeper AI!
echo.
pause
'''
    
    with open('Play_Minesweeper_Pro.bat', 'w') as f:
        f.write(installer_content)
    
    print("✅ Created Play_Minesweeper_Pro.bat")


def create_production_readme():
    """Create comprehensive README for production version."""
    readme_content = '''# Minesweeper AI - Production Edition v1.0

A professional-grade Minesweeper game with advanced AI assistant, comprehensive features, and production-ready reliability.

## 🚀 Quick Start

### Option 1: Easy Launch (Recommended)
- Double-click `Play_Minesweeper_Pro.bat`

### Option 2: Direct Launch
- Double-click `MinesweeperAI_Pro.exe`

## 🎮 Game Features

### Core Gameplay
- **5 Difficulty Levels**: Beginner, Easy, Medium, Hard, Expert
- **Professional Interface**: Clean, intuitive terminal-based design
- **Real-time Statistics**: Track your performance over time
- **Configuration System**: Customize your experience

### AI Assistant
- **Basic Logical Deduction**: Rules 1 & 2 for certain mine/safe identification
- **Constraint Satisfaction**: Advanced subset analysis for complex patterns
- **Probability Analysis**: Exact probability calculations for optimal guessing
- **Real-time Hints**: Shows certain mines, safe cells, and best guesses

### Professional Features
- **Error Handling**: Comprehensive error recovery and logging
- **Auto-save**: Automatic statistics and configuration saving
- **Multiple Game Modes**: Choose your preferred difficulty
- **Performance Tracking**: Detailed statistics and win rates
- **Customizable Settings**: Toggle AI, colors, and other features

## 🎯 How to Play

### Main Menu Options
1. **New Game** - Start a fresh game
2. **Change Difficulty** - Select from 5 difficulty levels
3. **View Statistics** - See your performance metrics
4. **Settings** - Configure game options
5. **Help** - View detailed instructions
6. **Exit** - Close the application

### In-Game Commands
- `r row col` - Reveal cell at (row, col)
- `c row col` - Clear cell (same as reveal)
- `f row col` - Flag/unflag cell at (row, col)
- `a` - Show AI suggestions and analysis
- `s` - Show current statistics
- `m` - Return to main menu
- `q` - Quit current game

### Difficulty Levels
- **Beginner**: 8x8 board, 10 mines
- **Easy**: 10x10 board, 15 mines
- **Medium**: 12x12 board, 25 mines
- **Hard**: 16x16 board, 40 mines
- **Expert**: 20x20 board, 80 mines

## 📊 Statistics Tracking

The game automatically tracks:
- Games played and won
- Win rate percentage
- Best completion time
- Average completion time
- Total mines cleared
- Flags placed
- AI suggestions used

## ⚙️ Settings

Customize your experience:
- **AI Assistant**: Enable/disable AI suggestions
- **Colors**: Enable/disable color coding
- **Auto-save**: Enable/disable automatic saving

## 🗂️ File Locations

Configuration and statistics are stored in:
```
%USERPROFILE%\\.minesweeper_ai\\
├── config.json      # Game settings
├── stats.json        # Game statistics
└── logs/            # Application logs
```

## 🔧 Technical Specifications

- **Version**: 1.0.0 Production
- **Platform**: Windows 10/11
- **Language**: Python 3.14
- **AI Engine**: Advanced constraint satisfaction and probability analysis
- **Interface**: Professional terminal-based with color support
- **Dependencies**: None (fully self-contained executable)
- **Size**: ~10 MB

## 🐛 Troubleshooting

### Common Issues
1. **Game won't start**: Check Windows Defender or antivirus
2. **No colors**: Use Settings menu to disable colors if needed
3. **Performance issues**: Try lower difficulty levels

### Error Logs
If you encounter issues, check the log files at:
`%USERPROFILE%\\.minesweeper_ai\\logs\\`

### Support
For issues or suggestions, check the log files and report the error details.

## 📝 Legend

- `.` - Unknown cell
- `F` - Flagged mine
- `*` - Mine (revealed)
- `1-8` - Number of adjacent mines (color-coded)

## 🏆 Tips for Success

1. **Start Smart**: Begin with corners or edge cells
2. **Use AI**: Press 'a' for intelligent suggestions when stuck
3. **Flag First**: Mark certain mines before revealing safe cells
4. **Pattern Recognition**: Learn common mine patterns
5. **Probability**: When uncertain, choose cells with lowest mine probability

## 📈 AI Intelligence Levels

The AI assistant provides:
- **Certain Solutions**: 100% accurate mine/safe identification
- **Probabilistic Analysis**: Risk assessment for uncertain cells
- **Optimal Strategy**: Mathematically best moves
- **Pattern Recognition**: Complex constraint satisfaction

---

**Minesweeper AI - Production Edition v1.0**  
*Professional gaming with artificial intelligence*

Built with precision and intelligence for the ultimate Minesweeper experience.
'''
    
    with open('README_PRODUCTION.md', 'w', encoding='utf-8') as f:
        f.write(readme_content)
    
    print("✅ Created README_PRODUCTION.md")


def create_version_info():
    """Create version information file."""
    version_info = '''# Version Information
VERSION = "1.0.0"
BUILD_DATE = "2024-02-15"
EDITION = "Production"
FEATURES = ["AI Assistant", "Statistics", "Multiple Difficulties", "Professional UI"]
'''
    
    with open('version.py', 'w') as f:
        f.write(version_info)
    
    print("✅ Created version.py")


def main():
    """Main production build process."""
    print("🏭 Building Production Minesweeper AI")
    print("=" * 60)
    
    # Check if we're in the right directory
    if not os.path.exists('production_minesweeper.py'):
        print("❌ production_minesweeper.py not found in current directory")
        return
    
    # Create supporting files
    create_version_info()
    create_production_spec()
    create_installer_script()
    create_production_readme()
    
    # Build executable
    if not build_production_executable():
        return
    
    # Check if executable was created
    exe_path = Path('dist/MinesweeperAI_Pro.exe')
    if exe_path.exists():
        print(f"\n🎉 PRODUCTION BUILD SUCCESSFUL!")
        print(f"Executable: {exe_path.absolute()}")
        
        # Move to current directory for convenience
        shutil.move('dist/MinesweeperAI_Pro.exe', 'MinesweeperAI_Pro.exe')
        shutil.rmtree('dist')
        
        print(f"\n📦 Production Package Contents:")
        print("  ✅ MinesweeperAI_Pro.exe - Main executable")
        print("  ✅ Play_Minesweeper_Pro.bat - Professional launcher")
        print("  ✅ README_PRODUCTION.md - Comprehensive documentation")
        print("  ✅ version.py - Version information")
        
        file_size = os.path.getsize('MinesweeperAI_Pro.exe') / (1024 * 1024)  # MB
        print(f"\n📊 Executable size: {file_size:.1f} MB")
        
        print(f"\n🚀 Ready for production distribution!")
        print(f"Share these files with end users:")
        print(f"  - MinesweeperAI_Pro.exe")
        print(f"  - Play_Minesweeper_Pro.bat")
        print(f"  - README_PRODUCTION.md")
        
        print(f"\n✨ Production Features:")
        print(f"  - Professional error handling")
        print(f"  - Comprehensive logging")
        print(f"  - Statistics tracking")
        print(f"  - Configuration system")
        print(f"  - Multiple difficulty levels")
        print(f"  - Advanced AI assistant")
        
    else:
        print("❌ Production executable was not created successfully")


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
