# Minesweeper AI - Terminal Game

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
