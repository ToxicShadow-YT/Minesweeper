#!/usr/bin/env python3
"""
Terminal Minesweeper with AI Assistant 🕵️‍♂️💣

A fully playable Minesweeper game in the terminal with AI assistance.
No pygame required!
"""

import os
import random
import sys
from typing import List, Tuple, Optional
from advanced_solver import AdvancedMinesweeperAI


class TerminalMinesweeper:
    """Terminal-based Minesweeper game with AI assistance."""
    
    def __init__(self, rows: int = 10, cols: int = 10, mines: int = 15):
        self.rows = rows
        self.cols = cols
        self.mines = mines
        self.board = [[-1 for _ in range(cols)] for _ in range(rows)]
        self.mine_positions = set()
        self.game_over = False
        self.game_won = False
        self.first_click = True
        self.flags = set()
        
        # Colors for terminal output
        self.COLORS = {
            'reset': '\033[0m',
            'red': '\033[91m',
            'green': '\033[92m',
            'yellow': '\033[93m',
            'blue': '\033[94m',
            'magenta': '\033[95m',
            'cyan': '\033[96m',
            'white': '\033[97m',
            'bold': '\033[1m',
            'underline': '\033[4m'
        }
        
        self.number_colors = {
            1: self.COLORS['blue'],
            2: self.COLORS['green'],
            3: self.COLORS['red'],
            4: self.COLORS['magenta'],
            5: self.COLORS['yellow'],
            6: self.COLORS['cyan'],
            7: self.COLORS['white'],
            8: self.COLORS['white']
        }
    
    def clear_screen(self):
        """Clear the terminal screen."""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def get_neighbors(self, r: int, c: int) -> List[Tuple[int, int]]:
        """Get all valid neighboring cells."""
        neighbors = []
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if dr == 0 and dc == 0:
                    continue
                nr, nc = r + dr, c + dc
                if 0 <= nr < self.rows and 0 <= nc < self.cols:
                    neighbors.append((nr, nc))
        return neighbors
    
    def place_mines(self, safe_row: int, safe_col: int):
        """Place mines randomly, avoiding the first clicked cell."""
        positions = [(r, c) for r in range(self.rows) for c in range(self.cols)]
        positions.remove((safe_row, safe_col))
        self.mine_positions = set(random.sample(positions, self.mines))
    
    def calculate_numbers(self):
        """Calculate numbers for each cell."""
        self.internal_board = [[0 for _ in range(self.cols)] for _ in range(self.rows)]
        
        for r, c in self.mine_positions:
            self.internal_board[r][c] = -1  # Mark mines
        
        for r in range(self.rows):
            for c in range(self.cols):
                if self.internal_board[r][c] != -1:
                    count = 0
                    for nr, nc in self.get_neighbors(r, c):
                        if self.internal_board[nr][nc] == -1:
                            count += 1
                    self.internal_board[r][c] = count
    
    def reveal_cell(self, r: int, c: int) -> bool:
        """Reveal a cell and return True if safe, False if mine."""
        if (r, c) in self.mine_positions:
            self.board[r][c] = 'M'
            self.game_over = True
            return False
        
        # Reveal the cell
        self.board[r][c] = self.internal_board[r][c]
        
        # If it's a 0, reveal all adjacent cells
        if self.internal_board[r][c] == 0:
            to_reveal = [(r, c)]
            revealed = set()
            
            while to_reveal:
                cr, cc = to_reveal.pop()
                if (cr, cc) in revealed:
                    continue
                revealed.add((cr, cc))
                
                for nr, nc in self.get_neighbors(cr, cc):
                    if self.board[nr][nc] == -1 and (nr, nc) not in self.mine_positions:
                        self.board[nr][nc] = self.internal_board[nr][nc]
                        if self.internal_board[nr][nc] == 0:
                            to_reveal.append((nr, nc))
        
        # Check win condition
        unknown_count = sum(1 for r in range(self.rows) for c in range(self.cols) 
                          if self.board[r][c] == -1)
        if unknown_count == len(self.mine_positions):
            self.game_won = True
        
        return True
    
    def toggle_flag(self, r: int, c: int):
        """Toggle flag on a cell."""
        if self.board[r][c] == -1:
            if (r, c) in self.flags:
                self.flags.remove((r, c))
            else:
                self.flags.add((r, c))
    
    def get_ai_suggestions(self):
        """Get AI suggestions for current board state."""
        # Create a copy of the board for the AI
        ai_board = [row[:] for row in self.board]
        
        # Convert flags to 'F' for AI
        for r, c in self.flags:
            if ai_board[r][c] == -1:
                ai_board[r][c] = 'F'
        
        ai = AdvancedMinesweeperAI(ai_board)
        mines, safe, probs = ai.solve()
        
        return mines, safe, probs
    
    def draw_board(self, show_mines: bool = False):
        """Draw the game board."""
        print(f"\n{self.COLORS['bold']}   MINESWEEPER 🕵️‍♂️💣{self.COLORS['reset']}")
        print(f"   Mines: {self.mines - len(self.flags)} | Flags: {len(self.flags)}")
        print()
        
        # Column headers
        print("   " + " ".join(f"{c:2}" for c in range(self.cols)))
        print("   " + "---" * self.cols)
        
        for r in range(self.rows):
            # Row header
            print(f"{r:2} |", end="")
            
            for c in range(self.cols):
                cell_value = self.board[r][c]
                
                if cell_value == -1:  # Unknown
                    if (r, c) in self.flags:
                        print(f"{self.COLORS['red']} F {self.COLORS['reset']}", end="")
                    else:
                        print(" . ", end="")
                
                elif cell_value == 'M':  # Mine
                    if show_mines or self.game_over:
                        print(f"{self.COLORS['red']}💣{self.COLORS['reset']} ", end="")
                    else:
                        print(" . ", end="")
                
                elif isinstance(cell_value, int):  # Number
                    if cell_value == 0:
                        print("   ", end="")
                    else:
                        color = self.number_colors.get(cell_value, self.COLORS['white'])
                        print(f"{color}{cell_value:2} {self.COLORS['reset']}", end="")
            
            print("|")
        
        print("   " + "---" * self.cols)
    
    def show_ai_hints(self):
        """Show AI hints on the board."""
        mines, safe, probs = self.get_ai_suggestions()
        
        print(f"\n{self.COLORS['cyan']}🤖 AI Analysis:{self.COLORS['reset']}")
        print(f"   Mines found: {len(mines)}")
        print(f"   Safe cells: {len(safe)}")
        
        if mines:
            print(f"\n{self.COLORS['red']}🚩 Certain Mines:{self.COLORS['reset']}")
            for r, c in sorted(mines):
                print(f"   ({r}, {c})")
        
        if safe:
            print(f"\n{self.COLORS['green']}✅ Safe Cells:{self.COLORS['reset']}")
            for r, c in sorted(safe):
                print(f"   ({r}, {c})")
        
        if probs and not mines and not safe:
            print(f"\n{self.COLORS['yellow']}📊 Best Guesses (lowest mine probability):{self.COLORS['reset']}")
            sorted_probs = sorted(probs.items(), key=lambda x: x[1])[:5]
            for (r, c), prob in sorted_probs:
                status = "SAFE" if prob < 0.1 else "RISKY" if prob > 0.5 else "MODERATE"
                print(f"   ({r}, {c}): {prob:.3f} - {status}")
    
    def get_input(self):
        """Get user input."""
        while True:
            try:
                cmd = input(f"\n{self.COLORS['bold']}Command (r/c/f/a/h/q): {self.COLORS['reset']}").strip().lower()
                
                if cmd == 'q':
                    return 'quit', None, None
                elif cmd == 'h':
                    return 'help', None, None
                elif cmd == 'a':
                    return 'ai', None, None
                else:
                    parts = cmd.split()
                    if len(parts) >= 3:
                        action = parts[0]
                        r = int(parts[1])
                        c = int(parts[2])
                        
                        if action in ['r', 'c', 'f'] and 0 <= r < self.rows and 0 <= c < self.cols:
                            return action, r, c
                        
                        print(f"{self.COLORS['red']}Invalid input!{self.COLORS['reset']}")
                    else:
                        print(f"{self.COLORS['red']}Invalid format! Use: action row col{self.COLORS['reset']}")
                        print(f"Actions: r(eveal), c(lear), f(lag)")
            
            except (ValueError, IndexError):
                print(f"{self.COLORS['red']}Invalid input!{self.COLORS['reset']}")
    
    def show_help(self):
        """Show help information."""
        self.clear_screen()
        print(f"{self.COLORS['bold']}🎮 MINESWEEPER HELP{self.COLORS['reset']}")
        print("=" * 50)
        print()
        print("COMMANDS:")
        print("  r row col  - Reveal cell at (row, col)")
        print("  c row col  - Clear cell (same as reveal)")
        print("  f row col  - Flag/unflag cell at (row, col)")
        print("  a          - Show AI suggestions")
        print("  h          - Show this help")
        print("  q          - Quit game")
        print()
        print("EXAMPLES:")
        print("  r 5 3     - Reveal cell at row 5, column 3")
        print("  f 2 7     - Flag cell at row 2, column 7")
        print()
        print("SYMBOLS:")
        print("  .  - Unknown cell")
        print("  F  - Flagged mine")
        print("  💣 - Mine (revealed)")
        print("  1-8 - Number of adjacent mines")
        print()
        print("AI FEATURES:")
        print("  - Logical deduction (Rules 1 & 2)")
        print("  - Constraint satisfaction")
        print("  - Probability analysis")
        print("  - Optimal guessing suggestions")
        print()
        input(f"{self.COLORS['yellow']}Press Enter to continue...{self.COLORS['reset']}")
    
    def play(self):
        """Main game loop."""
        self.clear_screen()
        print(f"{self.COLORS['bold']}🎮 WELCOME TO TERMINAL MINESWEEPER!{self.COLORS['reset']}")
        print(f"{self.COLORS['cyan']}With AI Assistant 🤖{self.COLORS['reset']}")
        print()
        print(f"Board: {self.rows}x{self.cols} | Mines: {self.mines}")
        print()
        self.show_help()
        
        while not self.game_over and not self.game_won:
            self.clear_screen()
            self.draw_board()
            
            if self.game_over:
                print(f"\n{self.COLORS['red']}{self.COLORS['bold']}💥 GAME OVER! 💥{self.COLORS['reset']}")
                self.draw_board(show_mines=True)
                break
            
            if self.game_won:
                print(f"\n{self.COLORS['green']}{self.COLORS['bold']}🎉 YOU WIN! 🎉{self.COLORS['reset']}")
                self.draw_board(show_mines=True)
                break
            
            action, r, c = self.get_input()
            
            if action == 'quit':
                print(f"{self.COLORS['yellow']}Game aborted.{self.COLORS['reset']}")
                break
            
            elif action == 'help':
                self.show_help()
                continue
            
            elif action == 'ai':
                self.show_ai_hints()
                input(f"\n{self.COLORS['yellow']}Press Enter to continue...{self.COLORS['reset']}")
                continue
            
            elif action in ['r', 'c']:  # Reveal
                if self.first_click:
                    self.place_mines(r, c)
                    self.calculate_numbers()
                    self.first_click = False
                
                if self.board[r][c] == -1:
                    self.reveal_cell(r, c)
                else:
                    print(f"{self.COLORS['yellow']}Cell already revealed!{self.COLORS['reset']}")
                    input(f"{self.COLORS['yellow']}Press Enter to continue...{self.COLORS['reset']}")
            
            elif action == 'f':  # Flag
                self.toggle_flag(r, c)
        
        print(f"\n{self.COLORS['bold']}Thanks for playing! 🎮{self.COLORS['reset']}")


def main():
    """Main function."""
    # Colors for terminal output
    COLORS = {
        'reset': '\033[0m',
        'red': '\033[91m',
        'green': '\033[92m',
        'yellow': '\033[93m',
        'blue': '\033[94m',
        'magenta': '\033[95m',
        'cyan': '\033[96m',
        'white': '\033[97m',
        'bold': '\033[1m',
        'underline': '\033[4m'
    }
    
    print(f"{COLORS['bold']}🕵️‍♂️💣 TERMINAL MINESWEEPER WITH AI 💣🕵️‍♂️{COLORS['reset']}")
    print("=" * 60)
    
    # Game settings
    rows = 10
    cols = 10
    mines = 15
    
    try:
        print(f"\nStarting {rows}x{cols} game with {mines} mines...")
        game = TerminalMinesweeper(rows, cols, mines)
        game.play()
    
    except KeyboardInterrupt:
        print(f"\n\n{COLORS['yellow']}Game interrupted by user.{COLORS['reset']}")
    except Exception as e:
        print(f"\n{COLORS['red']}Error: {e}{COLORS['reset']}")


if __name__ == "__main__":
    main()
