@echo off
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
    echo Check the log files in %%USERPROFILE%%\.minesweeper_ai\
)

echo.
echo Thanks for playing Minesweeper AI Enhanced!
echo.
pause
