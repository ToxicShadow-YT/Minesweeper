@echo off
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
    echo Check the log files in %%USERPROFILE%%\.minesweeper_ai\
)

echo.
echo Thanks for playing Minesweeper AI GUI!
echo.
pause
