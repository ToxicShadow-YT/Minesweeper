@echo off
title Cyberpunk Minesweeper AI - Uninstaller
color 0C

echo.
echo ====================================================
echo    🤖 CYBERPUNK MINESWEEPER AI - UNINSTALLER
echo ====================================================
echo.
echo ⚠️ This will remove Cyberpunk Minesweeper AI from your system.
echo.

set /p confirm="Are you sure you want to continue? (Y/N): "
if /i not "%confirm%"=="Y" (
    echo ❌ Uninstallation cancelled.
    pause
    exit /b
)

echo.
echo 🗑️ Removing Cyberpunk Minesweeper AI...

REM Remove installation directory
if exist "%PROGRAMFILES%\CyberpunkMinesweeperAI" (
    echo 📁 Removing program files...
    rmdir /s /q "%PROGRAMFILES%\CyberpunkMinesweeperAI"
)

REM Remove desktop shortcut
if exist "%USERPROFILE%\Desktop\CyberpunkMinesweeperAI.lnk" (
    echo 🎯 Removing desktop shortcut...
    del "%USERPROFILE%\Desktop\CyberpunkMinesweeperAI.lnk"
)

REM Remove Start Menu shortcut
if exist "%APPDATA%\Microsoft\Windows\Start Menu\Programs\CyberpunkMinesweeperAI\CyberpunkMinesweeperAI.lnk" (
    echo 📋 Removing Start Menu shortcut...
    del "%APPDATA%\Microsoft\Windows\Start Menu\Programs\CyberpunkMinesweeperAI\CyberpunkMinesweeperAI.lnk"
    rmdir "%APPDATA%\Microsoft\Windows\Start Menu\Programs\CyberpunkMinesweeperAI"
)

REM Remove user data (optional)
echo.
set /p remove_data="Remove saved games and settings? (Y/N): "
if /i "%remove_data%"=="Y" (
    echo 🗑️ Removing user data...
    if exist "%USERPROFILE%\.cyberpunk_minesweeper" (
        rmdir /s /q "%USERPROFILE%\.cyberpunk_minesweeper"
    )
)

echo.
echo ✅ Uninstallation complete!
echo.
echo 🎉 Cyberpunk Minesweeper AI has been removed from your system.
echo.
pause
