#!/usr/bin/env python3
"""
Build Terminal Minesweeper as Windows Executable
Creates a standalone .exe file that can be run without Python installed
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path


def install_pyinstaller():
    """Install PyInstaller if not already installed."""
    try:
        import PyInstaller
        print("✅ PyInstaller already installed")
        return True
    except ImportError:
        print("📦 Installing PyInstaller...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])
            print("✅ PyInstaller installed successfully")
            return True
        except subprocess.CalledProcessError:
            print("❌ Failed to install PyInstaller")
            return False


def create_spec_file():
    """Create PyInstaller spec file with custom settings."""
    spec_content = '''
# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['terminal_minesweeper.py'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=[],
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
    name='MinesweeperAI',
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
    icon=None,
)
'''
    
    with open('minesweeper.spec', 'w') as f:
        f.write(spec_content)
    
    print("✅ Created PyInstaller spec file")


def build_executable():
    """Build the executable using PyInstaller."""
    print("🔨 Building executable...")
    
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
            '--name=MinesweeperAI',
            'terminal_minesweeper.py'
        ])
        
        print("✅ Executable built successfully!")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Build failed: {e}")
        return False


def create_installer_script():
    """Create a simple batch script for easy distribution."""
    batch_content = '''@echo off
title Minesweeper AI - Terminal Game
echo.
echo ========================================
echo    MINESWEEPER AI - Terminal Game
echo ========================================
echo.
echo Starting Minesweeper with AI Assistant...
echo.
MinesweeperAI.exe
echo.
echo Thanks for playing!
pause
'''
    
    with open('Run_Minesweeper.bat', 'w') as f:
        f.write(batch_content)
    
    print("✅ Created Run_Minesweeper.bat for easy execution")


def create_readme():
    """Create README for the executable package."""
    readme_content = '''# Minesweeper AI - Terminal Game

A fully functional Minesweeper game with AI assistant, packaged as a standalone executable.

## How to Run

### Option 1: Double-click the batch file
- Run Run_Minesweeper.bat for the best experience

### Option 2: Run directly
- Double-click MinesweeperAI.exe
- Or run from command line: MinesweeperAI.exe

## How to Play

### Commands:
- r row col - Reveal cell at (row, col)
- c row col - Clear cell (same as reveal)
- f row col - Flag/unflag cell at (row, col)
- a - Show AI suggestions and analysis
- h - Show help menu
- q - Quit game

### Examples:
r 5 3    # Reveal cell at row 5, column 3
f 2 7    # Flag cell at row 2, column 7
a         # Get AI assistance

## AI Features

The AI assistant includes:
- Basic Logical Deduction - Rules 1 & 2 for certain mine/safe identification
- Constraint Satisfaction - Advanced subset analysis for complex patterns
- Probability Analysis - Exact probability calculations for optimal guessing
- Real-time Hints - Shows certain mines, safe cells, and best guesses

## Game Settings

- Board Size: 10x10
- Number of Mines: 15
- AI Assistant: Always available

## Tips

1. Start by revealing a corner or edge cell
2. Use the AI assistant (a command) when stuck
3. Flag cells the AI identifies as certain mines
4. Reveal cells the AI identifies as safe
5. When uncertain, choose cells with lowest mine probability

## Technical Details

- Language: Python 3
- AI Engine: Advanced constraint satisfaction and probability analysis
- Interface: Terminal-based with color support
- Dependencies: None (packaged in executable)

## Legend

- . - Unknown cell
- F - Flagged mine
- * - Mine (revealed)
- 1-8 - Number of adjacent mines (color-coded)

Built with AI intelligence! Enjoy the game!
'''
    
    with open('README_EXECUTABLE.md', 'w', encoding='utf-8') as f:
        f.write(readme_content)
    
    print("✅ Created README_EXECUTABLE.md")


def main():
    """Main build process."""
    print("🔨 Building Minesweeper AI Executable")
    print("=" * 50)
    
    # Check if we're in the right directory
    if not os.path.exists('terminal_minesweeper.py'):
        print("❌ terminal_minesweeper.py not found in current directory")
        return
    
    # Install PyInstaller
    if not install_pyinstaller():
        return
    
    # Create spec file
    create_spec_file()
    
    # Build executable
    if not build_executable():
        return
    
    # Create supporting files
    create_installer_script()
    create_readme()
    
    # Check if executable was created
    exe_path = Path('dist/MinesweeperAI.exe')
    if exe_path.exists():
        print(f"\n🎉 SUCCESS! Executable created at: {exe_path.absolute()}")
        
        # Move to current directory for convenience
        shutil.move('dist/MinesweeperAI.exe', 'MinesweeperAI.exe')
        shutil.rmtree('dist')
        
        print("📦 Package contents:")
        print("  ✅ MinesweeperAI.exe - Main executable")
        print("  ✅ Run_Minesweeper.bat - Easy launcher")
        print("  ✅ README_EXECUTABLE.md - Instructions")
        
        file_size = os.path.getsize('MinesweeperAI.exe') / (1024 * 1024)  # MB
        print(f"\n📊 Executable size: {file_size:.1f} MB")
        
        print("\n🚀 Ready to distribute! Just share these files:")
        print("  - MinesweeperAI.exe")
        print("  - Run_Minesweeper.bat")
        print("  - README_EXECUTABLE.md")
        
    else:
        print("❌ Executable was not created successfully")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️ Build interrupted by user")
    except Exception as e:
        print(f"\n❌ Build failed with error: {e}")
    
    input("\nPress Enter to exit...")
