#!/usr/bin/env python3
"""
Production GUI Minesweeper with AI Assistant
Professional graphical version with tkinter (built-in Python library)
"""

import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import random
import json
import logging
from datetime import datetime
from pathlib import Path
from typing import List, Tuple, Optional, Dict, Any
from dataclasses import dataclass, asdict
from advanced_solver import AdvancedMinesweeperAI


@dataclass
class GameConfig:
    """Game configuration settings."""
    difficulty: str = "medium"
    rows: int = 10
    cols: int = 10
    mines: int = 15
    ai_enabled: bool = True
    sound_enabled: bool = False
    auto_save: bool = True


@dataclass
class GameStats:
    """Game statistics tracking."""
    games_played: int = 0
    games_won: int = 0
    total_time: float = 0.0
    best_time: float = float('inf')
    mines_cleared: int = 0
    flags_placed: int = 0
    ai_suggestions_used: int = 0
    win_rate: float = 0.0


class MinesweeperGUI:
    """Professional GUI Minesweeper with AI Assistant."""
    
    DIFFICULTY_PRESETS = {
        "beginner": {"rows": 8, "cols": 8, "mines": 10},
        "easy": {"rows": 10, "cols": 10, "mines": 15},
        "medium": {"rows": 12, "cols": 12, "mines": 25},
        "hard": {"rows": 16, "cols": 16, "mines": 40},
        "expert": {"rows": 20, "cols": 20, "mines": 80}
    }
    
    # Color scheme
    COLORS = {
        'bg': '#2b2b2b',
        'cell_unknown': '#4a4a4a',
        'cell_revealed': '#1e1e1e',
        'cell_mine': '#ff4444',
        'cell_flag': '#ffaa00',
        'cell_safe_hint': '#44ff44',
        'cell_mine_hint': '#ff8844',
        'border': '#555555',
        'text': '#ffffff',
        'numbers': [
            '#0080ff',  # 1 - blue
            '#00ff00',  # 2 - green
            '#ff0000',  # 3 - red
            '#000080',  # 4 - dark blue
            '#800000',  # 5 - dark red
            '#00ffff',  # 6 - cyan
            '#000000',  # 7 - black
            '#808080',  # 8 - gray
        ]
    }
    
    def __init__(self):
        self.setup_logging()
        self.config = self.load_config()
        self.stats = self.load_stats()
        
        # Create main window
        self.root = tk.Tk()
        self.root.title("Minesweeper AI - Production Edition")
        self.root.configure(bg=self.COLORS['bg'])
        self.root.resizable(False, False)
        
        # Game state
        self.setup_game()
        self.game_start_time = None
        self.timer_running = False
        
        # GUI elements
        self.buttons = []
        self.mine_label = None
        self.time_label = None
        self.status_label = None
        
        self.create_gui()
        self.logger.info("GUI Minesweeper initialized")
    
    def setup_logging(self):
        """Setup logging system."""
        log_dir = Path.home() / ".minesweeper_ai"
        log_dir.mkdir(exist_ok=True)
        
        log_file = log_dir / f"minesweeper_gui_{datetime.now().strftime('%Y%m%d')}.log"
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_file)
            ]
        )
        
        self.logger = logging.getLogger(__name__)
    
    def load_config(self) -> GameConfig:
        """Load configuration from file."""
        config_file = Path.home() / ".minesweeper_ai" / "config.json"
        
        try:
            if config_file.exists():
                with open(config_file, 'r') as f:
                    data = json.load(f)
                return GameConfig(**data)
        except Exception as e:
            self.logger.warning(f"Failed to load config: {e}")
        
        return GameConfig()
    
    def save_config(self):
        """Save configuration to file."""
        config_file = Path.home() / ".minesweeper_ai" / "config.json"
        config_file.parent.mkdir(exist_ok=True)
        
        try:
            with open(config_file, 'w') as f:
                json.dump(asdict(self.config), f, indent=2)
        except Exception as e:
            self.logger.error(f"Failed to save config: {e}")
    
    def load_stats(self) -> GameStats:
        """Load statistics from file."""
        stats_file = Path.home() / ".minesweeper_ai" / "stats.json"
        
        try:
            if stats_file.exists():
                with open(stats_file, 'r') as f:
                    data = json.load(f)
                return GameStats(**data)
        except Exception as e:
            self.logger.warning(f"Failed to load stats: {e}")
        
        return GameStats()
    
    def save_stats(self):
        """Save statistics to file."""
        stats_file = Path.home() / ".minesweeper_ai" / "stats.json"
        stats_file.parent.mkdir(exist_ok=True)
        
        try:
            if self.stats.games_played > 0:
                self.stats.win_rate = (self.stats.games_won / self.stats.games_played) * 100
            
            with open(stats_file, 'w') as f:
                json.dump(asdict(self.stats), f, indent=2)
        except Exception as e:
            self.logger.error(f"Failed to save stats: {e}")
    
    def setup_game(self):
        """Setup game board based on configuration."""
        preset = self.DIFFICULTY_PRESETS.get(self.config.difficulty, {})
        self.rows = preset.get("rows", self.config.rows)
        self.cols = preset.get("cols", self.config.cols)
        self.mines = preset.get("mines", self.config.mines)
        
        self.board = [[-1 for _ in range(self.cols)] for _ in range(self.rows)]
        self.mine_positions = set()
        self.game_over = False
        self.game_won = False
        self.first_click = True
        self.flags = set()
        self.revealed_count = 0
        self.ai_hints = {'mines': set(), 'safe': set(), 'probs': {}}
        
        self.logger.info(f"Game setup: {self.rows}x{self.cols} with {self.mines} mines")
    
    def create_gui(self):
        """Create the GUI interface."""
        # Top frame for controls
        top_frame = ttk.Frame(self.root)
        top_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # Difficulty selector
        ttk.Label(top_frame, text="Difficulty:").pack(side=tk.LEFT, padx=5)
        self.difficulty_var = tk.StringVar(value=self.config.difficulty)
        difficulty_menu = ttk.Combobox(top_frame, textvariable=self.difficulty_var, 
                                      values=list(self.DIFFICULTY_PRESETS.keys()), 
                                      state="readonly", width=10)
        difficulty_menu.pack(side=tk.LEFT, padx=5)
        difficulty_menu.bind('<<ComboboxSelected>>', self.change_difficulty)
        
        # Control buttons
        ttk.Button(top_frame, text="New Game", command=self.new_game).pack(side=tk.LEFT, padx=5)
        ttk.Button(top_frame, text="AI Hints", command=self.show_ai_hints).pack(side=tk.LEFT, padx=5)
        ttk.Button(top_frame, text="Stats", command=self.show_stats).pack(side=tk.LEFT, padx=5)
        ttk.Button(top_frame, text="Settings", command=self.show_settings).pack(side=tk.LEFT, padx=5)
        
        # Status frame
        status_frame = ttk.Frame(self.root)
        status_frame.pack(fill=tk.X, padx=10, pady=5)
        
        self.mine_label = ttk.Label(status_frame, text=f"Mines: {self.mines}")
        self.mine_label.pack(side=tk.LEFT, padx=10)
        
        self.time_label = ttk.Label(status_frame, text="Time: 0s")
        self.time_label.pack(side=tk.LEFT, padx=10)
        
        self.status_label = ttk.Label(status_frame, text="Ready to play!")
        self.status_label.pack(side=tk.LEFT, padx=10)
        
        # Game board frame
        self.board_frame = ttk.Frame(self.root)
        self.board_frame.pack(padx=10, pady=10)
        
        self.create_board()
        
        # Start timer update
        self.update_timer()
    
    def create_board(self):
        """Create the game board buttons."""
        # Clear existing buttons
        for widget in self.board_frame.winfo_children():
            widget.destroy()
        
        self.buttons = []
        
        for r in range(self.rows):
            button_row = []
            for c in range(self.cols):
                btn = tk.Button(self.board_frame, width=2, height=1,
                              bg=self.COLORS['cell_unknown'],
                              fg=self.COLORS['text'],
                              font=('Arial', 10, 'bold'),
                              relief=tk.RAISED,
                              bd=2)
                btn.grid(row=r, column=c, padx=1, pady=1)
                btn.bind('<Button-1>', lambda e, row=r, col=c: self.left_click(row, col))
                btn.bind('<Button-3>', lambda e, row=r, col=c: self.right_click(row, col))
                button_row.append(btn)
            self.buttons.append(button_row)
    
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
        """Place mines randomly, avoiding first clicked cell."""
        positions = [(r, c) for r in range(self.rows) for c in range(self.cols)]
        positions.remove((safe_row, safe_col))
        
        try:
            self.mine_positions = set(random.sample(positions, self.mines))
            self.logger.debug(f"Mines placed at: {self.mine_positions}")
        except ValueError as e:
            self.logger.error(f"Failed to place mines: {e}")
            raise
    
    def calculate_numbers(self):
        """Calculate numbers for each cell."""
        self.internal_board = [[0 for _ in range(self.cols)] for _ in range(self.rows)]
        
        for r, c in self.mine_positions:
            self.internal_board[r][c] = -1
        
        for r in range(self.rows):
            for c in range(self.cols):
                if self.internal_board[r][c] != -1:
                    count = sum(1 for nr, nc in self.get_neighbors(r, c) 
                               if (nr, nc) in self.mine_positions)
                    self.internal_board[r][c] = count
    
    def left_click(self, r: int, c: int, event=None):
        """Handle left click on cell."""
        if self.game_over or self.game_won:
            return
        
        if self.board[r][c] != -1:
            return
        
        if self.first_click:
            self.place_mines(r, c)
            self.calculate_numbers()
            self.first_click = False
            self.game_start_time = datetime.now().timestamp()
            self.timer_running = True
            self.logger.info("Game started")
        
        self.reveal_cell(r, c)
    
    def right_click(self, r: int, c: int, event=None):
        """Handle right click on cell."""
        if self.game_over or self.game_won:
            return
        
        if self.board[r][c] != -1:
            return
        
        self.toggle_flag(r, c)
    
    def reveal_cell(self, r: int, c: int):
        """Reveal a cell."""
        try:
            if (r, c) in self.mine_positions:
                self.board[r][c] = 'M'
                self.game_over = True
                self.timer_running = False
                self.end_game(False)
                self.reveal_all_mines()
                self.logger.info(f"Game over: Mine hit at ({r}, {c})")
                return
            
            # Reveal the cell
            self.board[r][c] = self.internal_board[r][c]
            self.revealed_count += 1
            
            # Update button
            self.update_button(r, c)
            
            # If it's a 0, reveal all adjacent cells
            if self.internal_board[r][c] == 0:
                self.reveal_area(r, c)
            
            # Check win condition
            total_cells = self.rows * self.cols
            if self.revealed_count == total_cells - self.mines:
                self.game_won = True
                self.timer_running = False
                self.end_game(True)
                self.logger.info("Game won!")
            
        except Exception as e:
            self.logger.error(f"Error revealing cell ({r}, {c}): {e}")
    
    def reveal_area(self, r: int, c: int):
        """Reveal connected area of zeros."""
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
                    self.revealed_count += 1
                    self.update_button(nr, nc)
                    
                    if self.internal_board[nr][nc] == 0:
                        to_reveal.append((nr, nc))
    
    def toggle_flag(self, r: int, c: int):
        """Toggle flag on a cell."""
        if (r, c) in self.flags:
            self.flags.remove((r, c))
            self.buttons[r][c].config(text="", bg=self.COLORS['cell_unknown'])
        else:
            self.flags.add((r, c))
            self.stats.flags_placed += 1
            self.buttons[r][c].config(text="🚩", bg=self.COLORS['cell_flag'])
        
        self.update_mine_count()
    
    def update_button(self, r: int, c: int):
        """Update button appearance based on cell value."""
        value = self.board[r][c]
        btn = self.buttons[r][c]
        
        if value == 0:
            btn.config(text="", bg=self.COLORS['cell_revealed'], relief=tk.SUNKEN)
        elif isinstance(value, int) and value > 0:
            color = self.COLORS['numbers'][value - 1]
            btn.config(text=str(value), bg=self.COLORS['cell_revealed'], 
                      fg=color, relief=tk.SUNKEN)
    
    def reveal_all_mines(self):
        """Reveal all mines when game is over."""
        for r, c in self.mine_positions:
            self.buttons[r][c].config(text="💣", bg=self.COLORS['cell_mine'], 
                                     fg=self.COLORS['text'], relief=tk.SUNKEN)
    
    def update_mine_count(self):
        """Update mine counter."""
        remaining = self.mines - len(self.flags)
        self.mine_label.config(text=f"Mines: {remaining}")
    
    def update_timer(self):
        """Update game timer."""
        if self.timer_running and self.game_start_time:
            elapsed = int(datetime.now().timestamp() - self.game_start_time)
            self.time_label.config(text=f"Time: {elapsed}s")
        
        self.root.after(1000, self.update_timer)
    
    def end_game(self, won: bool):
        """Handle game end."""
        if self.game_start_time:
            game_time = datetime.now().timestamp() - self.game_start_time
            self.stats.total_time += game_time
            
            if won and (self.stats.best_time == float('inf') or game_time < self.stats.best_time):
                self.stats.best_time = game_time
        
        self.stats.games_played += 1
        if won:
            self.stats.games_won += 1
            self.stats.mines_cleared += len(self.mine_positions)
            self.status_label.config(text="🎉 YOU WIN! 🎉")
        else:
            self.status_label.config(text="💥 GAME OVER! 💥")
        
        if self.config.auto_save:
            self.save_stats()
    
    def new_game(self):
        """Start a new game."""
        self.setup_game()
        self.create_board()
        self.game_start_time = None
        self.timer_running = False
        self.update_mine_count()
        self.time_label.config(text="Time: 0s")
        self.status_label.config(text="Ready to play!")
        self.logger.info("New game started")
    
    def change_difficulty(self, event=None):
        """Change game difficulty."""
        self.config.difficulty = self.difficulty_var.get()
        self.save_config()
        self.new_game()
    
    def get_ai_suggestions(self):
        """Get AI suggestions for current board state."""
        if not self.config.ai_enabled:
            return set(), set(), {}
        
        try:
            ai_board = [row[:] for row in self.board]
            
            for r, c in self.flags:
                if ai_board[r][c] == -1:
                    ai_board[r][c] = 'F'
            
            ai = AdvancedMinesweeperAI(ai_board)
            mines, safe, probs = ai.solve()
            
            self.stats.ai_suggestions_used += 1
            return mines, safe, probs
            
        except Exception as e:
            self.logger.error(f"Error getting AI suggestions: {e}")
            return set(), set(), {}
    
    def show_ai_hints(self):
        """Show AI hints dialog."""
        mines, safe, probs = self.get_ai_suggestions()
        
        dialog = tk.Toplevel(self.root)
        dialog.title("AI Analysis")
        dialog.geometry("400x300")
        dialog.configure(bg=self.COLORS['bg'])
        
        # Title
        ttk.Label(dialog, text="🤖 AI Analysis", font=('Arial', 12, 'bold')).pack(pady=10)
        
        # Results
        ttk.Label(dialog, text=f"Certain Mines: {len(mines)}").pack(pady=5)
        ttk.Label(dialog, text=f"Safe Cells: {len(safe)}").pack(pady=5)
        
        # Mine locations
        if mines:
            ttk.Label(dialog, text="Certain Mines:", font=('Arial', 10, 'bold')).pack(pady=5)
            mine_text = ", ".join([f"({r},{c})" for r, c in sorted(mines)])
            ttk.Label(dialog, text=mine_text).pack(pady=5)
        
        # Safe cells
        if safe:
            ttk.Label(dialog, text="Safe Cells:", font=('Arial', 10, 'bold')).pack(pady=5)
            safe_text = ", ".join([f"({r},{c})" for r, c in sorted(safe)])
            ttk.Label(dialog, text=safe_text).pack(pady=5)
        
        # Probabilities
        if probs and not mines and not safe:
            ttk.Label(dialog, text="Best Guesses:", font=('Arial', 10, 'bold')).pack(pady=5)
            sorted_probs = sorted(probs.items(), key=lambda x: x[1])[:5]
            for (r, c), prob in sorted_probs:
                status = "SAFE" if prob < 0.1 else "RISKY" if prob > 0.5 else "MODERATE"
                ttk.Label(dialog, text=f"({r},{c}): {prob:.3f} - {status}").pack(pady=2)
        
        # Apply hints button
        if mines or safe:
            def apply_hints():
                for r, c in mines:
                    if self.board[r][c] == -1:
                        self.toggle_flag(r, c)
                for r, c in safe:
                    if self.board[r][c] == -1:
                        self.reveal_cell(r, c)
                dialog.destroy()
            
            ttk.Button(dialog, text="Apply Hints", command=apply_hints).pack(pady=10)
        
        ttk.Button(dialog, text="Close", command=dialog.destroy).pack(pady=5)
    
    def show_stats(self):
        """Show statistics dialog."""
        dialog = tk.Toplevel(self.root)
        dialog.title("Statistics")
        dialog.geometry("300x250")
        dialog.configure(bg=self.COLORS['bg'])
        
        ttk.Label(dialog, text="📊 Game Statistics", font=('Arial', 12, 'bold')).pack(pady=10)
        
        ttk.Label(dialog, text=f"Games Played: {self.stats.games_played}").pack(pady=5)
        ttk.Label(dialog, text=f"Games Won: {self.stats.games_won}").pack(pady=5)
        ttk.Label(dialog, text=f"Win Rate: {self.stats.win_rate:.1f}%").pack(pady=5)
        
        if self.stats.best_time != float('inf'):
            ttk.Label(dialog, text=f"Best Time: {self.stats.best_time:.1f}s").pack(pady=5)
        
        if self.stats.games_played > 0:
            avg_time = self.stats.total_time / self.stats.games_played
            ttk.Label(dialog, text=f"Average Time: {avg_time:.1f}s").pack(pady=5)
        
        ttk.Label(dialog, text=f"AI Suggestions Used: {self.stats.ai_suggestions_used}").pack(pady=5)
        
        ttk.Button(dialog, text="Close", command=dialog.destroy).pack(pady=10)
    
    def show_settings(self):
        """Show settings dialog."""
        dialog = tk.Toplevel(self.root)
        dialog.title("Settings")
        dialog.geometry("250x150")
        dialog.configure(bg=self.COLORS['bg'])
        
        ttk.Label(dialog, text="⚙️ Settings", font=('Arial', 12, 'bold')).pack(pady=10)
        
        # AI enabled
        ai_var = tk.BooleanVar(value=self.config.ai_enabled)
        ttk.Checkbutton(dialog, text="AI Assistant", variable=ai_var,
                       command=lambda: self.update_setting('ai_enabled', ai_var.get())).pack(pady=5)
        
        # Auto save
        save_var = tk.BooleanVar(value=self.config.auto_save)
        ttk.Checkbutton(dialog, text="Auto-save Statistics", variable=save_var,
                       command=lambda: self.update_setting('auto_save', save_var.get())).pack(pady=5)
        
        ttk.Button(dialog, text="Close", command=dialog.destroy).pack(pady=10)
    
    def update_setting(self, key: str, value: Any):
        """Update a setting."""
        setattr(self.config, key, value)
        self.save_config()
    
    def run(self):
        """Start the GUI application."""
        try:
            self.logger.info("GUI Minesweeper started")
            self.root.mainloop()
        except Exception as e:
            self.logger.critical(f"Fatal error: {e}")
            messagebox.showerror("Error", f"A critical error occurred: {e}")
        finally:
            self.save_config()
            self.save_stats()


def main():
    """Main entry point."""
    try:
        game = MinesweeperGUI()
        game.run()
    except Exception as e:
        print(f"Failed to start GUI game: {e}")
        messagebox.showerror("Error", f"Failed to start game: {e}")


if __name__ == "__main__":
    main()
