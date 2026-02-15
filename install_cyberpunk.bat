@echo off
title Cyberpunk Minesweeper AI - Installer
color 0A

echo.
echo ====================================================
echo    🤖 CYBERPUNK MINESWEEPER AI - INSTALLER
echo ====================================================
echo.
echo 🚀 Installing Cyberpunk Minesweeper AI Ultimate Edition...
echo.

REM Create installation directory
if not exist "%PROGRAMFILES%\CyberpunkMinesweeperAI" (
    mkdir "%PROGRAMFILES%\CyberpunkMinesweeperAI"
)

REM Copy files
echo 📦 Copying game files...
copy "CyberpunkMinesweeperAI.exe" "%PROGRAMFILES%\CyberpunkMinesweeperAI\" >nul
copy "Play_Cyberpunk_Minesweeper.bat" "%PROGRAMFILES%\CyberpunkMinesweeperAI\" >nul
copy "README_Cyberpunk.md" "%PROGRAMFILES%\CyberpunkMinesweeperAI\" >nul

REM Create desktop shortcut
echo 🎯 Creating desktop shortcut...
powershell "$WshShell = New-Object -comObject WScript.Shell; $Shortcut = $WshShell.CreateShortcut('%USERPROFILE%\Desktop\CyberpunkMinesweeperAI.lnk'); $Shortcut.TargetPath = '%PROGRAMFILES%\CyberpunkMinesweeperAI\Play_Cyberpunk_Minesweeper.bat'; $Shortcut.Save()"

REM Create Start Menu shortcut
echo 📋 Creating Start Menu shortcut...
if not exist "%APPDATA%\Microsoft\Windows\Start Menu\Programs\CyberpunkMinesweeperAI" (
    mkdir "%APPDATA%\Microsoft\Windows\Start Menu\Programs\CyberpunkMinesweeperAI"
)
powershell "$WshShell = New-Object -comObject WScript.Shell; $Shortcut = $WshShell.CreateShortcut('%APPDATA%\Microsoft\Windows\Start Menu\Programs\CyberpunkMinesweeperAI\CyberpunkMinesweeperAI.lnk'); $Shortcut.TargetPath = '%PROGRAMFILES%\CyberpunkMinesweeperAI\Play_Cyberpunk_Minesweeper.bat'; $Shortcut.Save()"

echo.
echo ✅ Installation complete!
echo.
echo 🎮 Launch options:
echo    • Desktop shortcut
echo    • Start Menu → CyberpunkMinesweeperAI
echo    • Direct: %PROGRAMFILES%\CyberpunkMinesweeperAI\Play_Cyberpunk_Minesweeper.bat
echo.
echo 🎉 Enjoy Cyberpunk Minesweeper AI!
echo.
pause
