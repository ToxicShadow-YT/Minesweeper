@echo off
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
    echo Check the log files in %%USERPROFILE%%\.minesweeper_ai\
)

echo.
echo Thanks for playing Minesweeper AI!
echo.
pause
