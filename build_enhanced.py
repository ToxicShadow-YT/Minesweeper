#!/usr/bin/env python3
"""
Build Enhanced GUI Minesweeper Executable
Creates the ultimate version with improved UI and auto-solver
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path


def build_enhanced_executable():
    """Build the enhanced GUI executable."""
    print("🚀 Building Enhanced GUI Minesweeper...")
    
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
            '--name=MinesweeperAI_Enhanced',
            'enhanced_gui.py'
        ])
        
        print("✅ Enhanced GUI executable built successfully!")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Build failed: {e}")
        return False


def create_enhanced_launcher():
    """Create enhanced GUI launcher script."""
    launcher_content = '''@echo off
title Minesweeper AI - Enhanced Edition
color 0B

echo.
echo ====================================================
echo    MINESWEEPER AI - Enhanced Edition v2.0
echo ====================================================
echo.
echo Ultimate Minesweeper with AI Auto-Solver
echo Features:
echo   - Enhanced graphical interface
echo   - Multiple themes (Dark, Light, Blue)
echo   - AI Auto-Solver with visual progress
echo   - Animated cell reveals
echo   - Hover effects and visual feedback
echo   - Advanced AI with probability analysis
echo   - Real-time statistics tracking
echo   - Professional UI with icons
echo.
echo Starting enhanced game...
echo.

MinesweeperAI_Enhanced.exe

if errorlevel 1 (
    echo.
    echo An error occurred while running the game.
    echo Check the log files in %%USERPROFILE%%\\.minesweeper_ai\\
)

echo.
echo Thanks for playing Minesweeper AI Enhanced!
echo.
pause
'''
    
    with open('Play_Minesweeper_Enhanced.bat', 'w') as f:
        f.write(launcher_content)
    
    print("✅ Created Play_Minesweeper_Enhanced.bat")


def create_enhanced_readme():
    """Create README for enhanced version."""
    readme_content = '''# Minesweeper AI - Enhanced Edition v2.0

The ultimate Minesweeper experience with professional GUI, AI auto-solver, and enhanced visual features.

## 🚀 Quick Start

### Option 1: Easy Launch (Recommended)
- Double-click `Play_Minesweeper_Enhanced.bat`

### Option 2: Direct Launch
- Double-click `MinesweeperAI_Enhanced.exe`

## 🎮 Enhanced Features

### 🎨 Professional UI Design
- **Multiple Themes**: Dark, Light, and Blue color schemes
- **Hover Effects**: Visual feedback on mouse interaction
- **Animated Reveals**: Smooth cell reveal animations
- **Professional Icons**: Emoji icons for better visual appeal
- **Progress Bar**: Visual progress during auto-solve
- **Responsive Layout**: Adapts to different board sizes

### 🤖 AI Auto-Solver
- **One-Click Solving**: Press "Auto-Solve" to watch AI play
- **Visual Progress**: Progress bar shows solving completion
- **Speed Control**: Choose from Slow, Medium, Fast, or Instant
- **Threaded Operation**: Non-blocking auto-solve with smooth UI
- **Intelligent Moves**: Uses all AI techniques (logic, constraints, probability)
- **Stop Anytime**: Cancel auto-solve at any point

### 🎯 Enhanced Gameplay
- **Improved Visuals**: Better color contrast and readability
- **Cell Highlighting**: Hover effects for better interaction
- **Smooth Animations**: Flash effects for safe cell reveals
- **Professional Styling**: Modern, polished appearance
- **Better Feedback**: Clear status messages and indicators

### 📊 Advanced Statistics
- **Auto-Solve Tracking**: Count of completed auto-solves
- **Enhanced Metrics**: More detailed performance statistics
- **Visual Display**: Professional statistics dialog
- **Performance History**: Track improvement over time

## 🎮 How to Play

### Basic Controls
- **Left Click**: Reveal cell
- **Right Click**: Place/remove flag
- **Hover**: Visual cell highlighting

### Enhanced Features
- **Theme Selector**: Switch between Dark, Light, and Blue themes
- **Speed Control**: Adjust auto-solve animation speed
- **Auto-Solve Button**: Watch AI solve the puzzle automatically
- **Progress Bar**: Visual feedback during auto-solve

### AI Integration
- **AI Hints**: Get intelligent suggestions
- **Auto-Solve**: Complete puzzle solving automation
- **Probability Analysis**: Risk assessment for uncertain cells
- **Real-time Analysis**: AI help available anytime

## 🎨 Theme Options

### Dark Theme (Default)
- Professional dark interface
- High contrast for visibility
- Easy on the eyes

### Light Theme
- Clean, bright interface
- Classic appearance
- Good for well-lit environments

### Blue Theme
- Modern blue color scheme
- Professional appearance
- Distinctive visual style

## ⚡ Auto-Solver Features

### Speed Settings
- **Slow**: 1.0 second delay between moves
- **Medium**: 0.5 second delay between moves
- **Fast**: 0.2 second delay between moves
- **Instant**: 0.05 second delay (nearly instant)

### AI Techniques Used
1. **Basic Logical Deduction** (Rules 1 & 2)
2. **Constraint Satisfaction** (Subset analysis)
3. **Probability Analysis** (Optimal guessing)
4. **Pattern Recognition** (Complex scenarios)

### Visual Feedback
- **Progress Bar**: Shows completion percentage
- **Status Messages**: Real-time solving status
- **Animated Moves**: Visual cell reveals
- **Smooth Transitions**: Professional animations

## 📊 Enhanced Statistics

### Performance Metrics
- Games played and won
- Win rate percentage
- Best and average completion times
- AI suggestions used
- **Auto-solves completed** (NEW)
- Total flags placed

### Visual Display
- Professional statistics dialog
- Organized metric presentation
- Clear performance indicators

## 🔧 Technical Specifications

- **Version**: 2.0 Enhanced Edition
- **Platform**: Windows 10/11
- **Interface**: Enhanced Tkinter GUI
- **AI Engine**: Advanced multi-technique solver
- **Features**: Auto-solver, themes, animations
- **Dependencies**: None (fully self-contained)
- **Size**: ~12 MB

## 🎯 Enhanced Tips

### Auto-Solver Usage
1. Start a game and make your first move
2. Click "Auto-Solve" to watch AI play
3. Adjust speed with the speed selector
4. Watch the progress bar for completion
5. Stop anytime by starting a new game

### Theme Selection
- **Dark**: Best for low-light environments
- **Light**: Classic Minesweeper appearance
- **Blue**: Modern, professional look

### Performance Optimization
- Use "Instant" speed for quick solving
- Choose themes based on lighting conditions
- Enable auto-save for statistics persistence

## 🆚 Version Comparison

### Enhanced vs Standard GUI
- **Auto-Solver**: Complete puzzle automation
- **Themes**: Multiple color schemes
- **Animations**: Smooth visual effects
- **Progress Bar**: Visual solving feedback
- **Enhanced Stats**: Auto-solve tracking
- **Professional UI**: Modern, polished appearance

### Enhanced vs Terminal
- **Full GUI**: Complete visual interface
- **Auto-Solver**: Watch AI solve automatically
- **Themes**: Customizable appearance
- **Animations**: Professional visual effects
- **Progress Tracking**: Visual feedback
- **Modern Design**: Contemporary interface

## 🐛 Enhanced Troubleshooting

### Common Issues
1. **Auto-solver not working**: Make first move first
2. **Theme not applying**: Restart the application
3. **Animations lag**: Use "Fast" or "Instant" speed
4. **Progress not showing**: Check if auto-solve is active

### Performance Tips
- Use "Instant" speed for faster solving
- Choose lighter themes for better performance
- Close other applications for smoother animations

## 🏆 Ultimate Experience

The Enhanced Edition provides the complete Minesweeper experience:
- **Professional GUI** with modern design
- **AI Auto-Solver** for automated gameplay
- **Multiple Themes** for customization
- **Smooth Animations** for visual appeal
- **Advanced Statistics** for performance tracking
- **Complete Automation** for puzzle solving

---

**Minesweeper AI - Enhanced Edition v2.0**  
*The ultimate professional Minesweeper with AI auto-solver*

Experience the future of Minesweeper with complete automation, professional design, and intelligent AI assistance!
'''
    
    with open('README_ENHANCED.md', 'w', encoding='utf-8') as f:
        f.write(readme_content)
    
    print("✅ Created README_ENHANCED.md")


def main():
    """Main enhanced build process."""
    print("🚀 Building Enhanced GUI Minesweeper AI")
    print("=" * 60)
    
    # Check if we're in the right directory
    if not os.path.exists('enhanced_gui.py'):
        print("❌ enhanced_gui.py not found in current directory")
        return
    
    # Create supporting files
    create_enhanced_launcher()
    create_enhanced_readme()
    
    # Build executable
    if not build_enhanced_executable():
        return
    
    # Check if executable was created
    exe_path = Path('dist/MinesweeperAI_Enhanced.exe')
    if exe_path.exists():
        print(f"\n🎉 ENHANCED BUILD SUCCESSFUL!")
        print(f"Executable: {exe_path.absolute()}")
        
        # Move to current directory for convenience
        shutil.move('dist/MinesweeperAI_Enhanced.exe', 'MinesweeperAI_Enhanced.exe')
        shutil.rmtree('dist')
        
        print(f"\n📦 Enhanced Package Contents:")
        print("  ✅ MinesweeperAI_Enhanced.exe - Ultimate GUI executable")
        print("  ✅ Play_Minesweeper_Enhanced.bat - Enhanced launcher")
        print("  ✅ README_ENHANCED.md - Complete documentation")
        
        file_size = os.path.getsize('MinesweeperAI_Enhanced.exe') / (1024 * 1024)  # MB
        print(f"\n📊 Executable size: {file_size:.1f} MB")
        
        print(f"\n🚀 Ready for Enhanced distribution!")
        print(f"Share these files with end users:")
        print(f"  - MinesweeperAI_Enhanced.exe")
        print(f"  - Play_Minesweeper_Enhanced.bat")
        print(f"  - README_ENHANCED.md")
        
        print(f"\n✨ Enhanced Features:")
        print(f"  - 🤖 AI Auto-Solver with visual progress")
        print(f"  - 🎨 Multiple themes (Dark, Light, Blue)")
        print(f"  - ✨ Smooth animations and hover effects")
        print(f"  - 📊 Enhanced statistics with auto-solve tracking")
        print(f"  - ⚡ Speed control for auto-solve")
        print(f"  - 🎯 Professional UI with modern design")
        print(f"  - 🔄 Threaded non-blocking operations")
        
    else:
        print("❌ Enhanced executable was not created successfully")


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
