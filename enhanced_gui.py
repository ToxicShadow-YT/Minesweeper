#!/usr/bin/env python3
"""
Enhanced GUI Minesweeper with AI Auto-Solver
Professional version with improved UI and automatic solving capabilities
"""

import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import random
import json
import logging
import threading
import time
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
    animation_speed: float = 0.1
    theme: str = "dark"


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
    auto_solves_completed: int = 0
    win_rate: float = 0.0


class EnhancedMinesweeperGUI:
    """Enhanced GUI Minesweeper with improved UI and auto-solver."""
    
    DIFFICULTY_PRESETS = {
        "beginner": {"rows": 8, "cols": 8, "mines": 10},
        "easy": {"rows": 10, "cols": 10, "mines": 15},
        "medium": {"rows": 12, "cols": 12, "mines": 25},
        "hard": {"rows": 16, "cols": 16, "mines": 40},
        "expert": {"rows": 20, "cols": 20, "mines": 80}
    }
    
    # Enhanced color schemes
    THEMES = {
        "dark": {
            'bg': '#1e1e1e',
            'fg': '#ffffff',
            'cell_unknown': '#2d2d2d',
            'cell_revealed': '#0a0a0a',
            'cell_mine': '#ff4444',
            'cell_flag': '#ffaa00',
            'cell_safe_hint': '#44ff44',
            'cell_mine_hint': '#ff8844',
            'button_bg': '#3a3a3a',
            'button_fg': '#ffffff',
            'numbers': ['#0080ff', '#00ff00', '#ff0000', '#000080', '#800000', '#00ffff', '#000000', '#808080']
        },
        "light": {
            'bg': '#f0f0f0',
            'fg': '#000000',
            'cell_unknown': '#d0d0d0',
            'cell_revealed': '#ffffff',
            'cell_mine': '#ff0000',
            'cell_flag': '#ff8800',
            'cell_safe_hint': '#00ff00',
            'cell_mine_hint': '#ff6600',
            'button_bg': '#e0e0e0',
            'button_fg': '#000000',
            'numbers': ['#0000ff', '#008000', '#ff0000', '#000080', '#800000', '#008080', '#000000', '#808080']
        },
        "blue": {
            'bg': '#001f3f',
            'fg': '#ffffff',
            'cell_unknown': '#003366',
            'cell_revealed': '#002244',
            'cell_mine': '#ff4444',
            'cell_flag': '#ffaa00',
            'cell_safe_hint': '#44ff44',
            'cell_mine_hint': '#ff8844',
            'button_bg': '#004488',
            'button_fg': '#ffffff',
            'numbers': ['#00ddff', '#00ff88', '#ff8888', '#8800ff', '#ff8800', '#00ffff', '#ffffff', '#aaaaaa']
        }
    }
    
    def __init__(self):
        self.setup_logging()
        self.config = self.load_config()
        self.stats = self.load_stats()
        
        # Create main window
        self.root = tk.Tk()
        self.root.title("🤖 Minesweeper AI - Enhanced Edition")
        self.root.resizable(False, False)
        
        # Apply theme
        self.apply_theme()
        
        # Game state
        self.setup_game()
        self.game_start_time = None
        self.timer_running = False
        self.auto_solving = False
        self.animation_queue = []
        
        # GUI elements
        self.buttons = []
        self.mine_label = None
        self.time_label = None
        self.status_label = None
        self.progress_var = None
        self.progress_bar = None
        
        self.create_enhanced_gui()
        self.logger.info("Enhanced GUI Minesweeper initialized")
    
    def apply_theme(self):
        """Apply the selected theme to the window."""
        theme = self.THEMES[self.config.theme]
        self.root.configure(bg=theme['bg'])
        self.colors = theme
    
    def setup_logging(self):
        """Setup logging system."""
        log_dir = Path.home() / ".minesweeper_ai"
        log_dir.mkdir(exist_ok=True)
        
        log_file = log_dir / f"minesweeper_enhanced_{datetime.now().strftime('%Y%m%d')}.log"
        
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
    
    def create_enhanced_gui(self):
        """Create the enhanced GUI interface."""
        # Enhanced top frame with better styling
        top_frame = ttk.Frame(self.root)
        top_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # Style configuration
        style = ttk.Style()
        style.theme_use('clam')
        
        # Difficulty selector with enhanced styling
        ttk.Label(top_frame, text="🎯 Difficulty:", font=('Arial', 10, 'bold')).pack(side=tk.LEFT, padx=5)
        self.difficulty_var = tk.StringVar(value=self.config.difficulty)
        difficulty_menu = ttk.Combobox(top_frame, textvariable=self.difficulty_var, 
                                      values=list(self.DIFFICULTY_PRESETS.keys()), 
                                      state="readonly", width=12, font=('Arial', 9))
        difficulty_menu.pack(side=tk.LEFT, padx=5)
        difficulty_menu.bind('<<ComboboxSelected>>', self.change_difficulty)
        
        # Enhanced control buttons with icons
        ttk.Button(top_frame, text="🔄 New Game", command=self.new_game, width=12).pack(side=tk.LEFT, padx=3)
        ttk.Button(top_frame, text="🤖 AI Hints", command=self.show_ai_hints, width=12).pack(side=tk.LEFT, padx=3)
        ttk.Button(top_frame, text="⚡ Auto-Solve", command=self.start_auto_solve, width=12).pack(side=tk.LEFT, padx=3)
        ttk.Button(top_frame, text="📊 Stats", command=self.show_stats, width=8).pack(side=tk.LEFT, padx=3)
        ttk.Button(top_frame, text="⚙️ Settings", command=self.show_settings, width=10).pack(side=tk.LEFT, padx=3)
        
        # Enhanced status frame with progress bar
        status_frame = ttk.Frame(self.root)
        status_frame.pack(fill=tk.X, padx=10, pady=5)
        
        self.mine_label = ttk.Label(status_frame, text=f"💣 Mines: {self.mines}", font=('Arial', 10, 'bold'))
        self.mine_label.pack(side=tk.LEFT, padx=10)
        
        self.time_label = ttk.Label(status_frame, text="⏱️ Time: 0s", font=('Arial', 10, 'bold'))
        self.time_label.pack(side=tk.LEFT, padx=10)
        
        self.status_label = ttk.Label(status_frame, text="🎮 Ready to play!", font=('Arial', 10, 'bold'))
        self.status_label.pack(side=tk.LEFT, padx=10)
        
        # Progress bar for auto-solve
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(status_frame, variable=self.progress_var, 
                                          maximum=100, length=150, mode='determinate')
        self.progress_bar.pack(side=tk.LEFT, padx=10)
        self.progress_bar.pack_forget()  # Hide initially
        
        # Enhanced game board frame with better spacing
        self.board_frame = ttk.Frame(self.root)
        self.board_frame.pack(padx=15, pady=15)
        
        self.create_enhanced_board()
        
        # Bottom frame with additional controls
        bottom_frame = ttk.Frame(self.root)
        bottom_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # Theme selector
        ttk.Label(bottom_frame, text="🎨 Theme:", font=('Arial', 9)).pack(side=tk.LEFT, padx=5)
        self.theme_var = tk.StringVar(value=self.config.theme)
        theme_menu = ttk.Combobox(bottom_frame, textvariable=self.theme_var, 
                                  values=list(self.THEMES.keys()), 
                                  state="readonly", width=10, font=('Arial', 8))
        theme_menu.pack(side=tk.LEFT, padx=5)
        theme_menu.bind('<<ComboboxSelected>>', self.change_theme)
        
        # Speed control for auto-solve
        ttk.Label(bottom_frame, text="⚡ Speed:", font=('Arial', 9)).pack(side=tk.LEFT, padx=5)
        self.speed_var = tk.StringVar(value="Medium")
        speed_menu = ttk.Combobox(bottom_frame, textvariable=self.speed_var, 
                                   values=["Slow", "Medium", "Fast", "Instant"], 
                                   state="readonly", width=8, font=('Arial', 8))
        speed_menu.pack(side=tk.LEFT, padx=5)
        
        # Start timer update
        self.update_timer()
    
    def create_enhanced_board(self):
        """Create the enhanced game board with better styling."""
        # Clear existing buttons
        for widget in self.board_frame.winfo_children():
            widget.destroy()
        
        self.buttons = []
        
        # Calculate button size based on board dimensions
        btn_size = max(2, min(4, 40 // max(self.rows, self.cols)))
        
        for r in range(self.rows):
            button_row = []
            for c in range(self.cols):
                btn = tk.Button(self.board_frame, 
                              width=btn_size, height=btn_size,
                              bg=self.colors['cell_unknown'],
                              fg=self.colors['fg'],
                              font=('Arial', max(8, 12 - btn_size), 'bold'),
                              relief=tk.RAISED,
                              bd=2,
                              cursor="hand2")
                btn.grid(row=r, column=c, padx=1, pady=1)
                btn.bind('<Button-1>', lambda e, row=r, col=c: self.left_click(row, col))
                btn.bind('<Button-3>', lambda e, row=r, col=c: self.right_click(row, col))
                btn.bind('<Enter>', lambda e, row=r, col=c: self.on_cell_enter(row, col))
                btn.bind('<Leave>', lambda e, row=r, col=c: self.on_cell_leave(row, col))
                button_row.append(btn)
            self.buttons.append(button_row)
    
    def on_cell_enter(self, r: int, c: int, event=None):
        """Handle mouse enter on cell."""
        if self.game_over or self.game_won or self.board[r][c] != -1:
            return
        
        # Highlight cell on hover
        if (r, c) not in self.flags:
            self.buttons[r][c].config(bg=self.colors['button_bg'])
    
    def on_cell_leave(self, r: int, c: int, event=None):
        """Handle mouse leave on cell."""
        if self.game_over or self.game_won or self.board[r][c] != -1:
            return
        
        # Restore normal color
        if (r, c) not in self.flags:
            self.buttons[r][c].config(bg=self.colors['cell_unknown'])
    
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
        if self.game_over or self.game_won or self.auto_solving:
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
        if self.game_over or self.game_won or self.auto_solving:
            return
        
        if self.board[r][c] != -1:
            return
        
        self.toggle_flag(r, c)
    
    def reveal_cell(self, r: int, c: int, animate: bool = False):
        """Reveal a cell with optional animation."""
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
            
            # Update button with animation
            if animate:
                self.animate_reveal(r, c)
            else:
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
    
    def animate_reveal(self, r: int, c: int):
        """Animate cell revelation."""
        btn = self.buttons[r][c]
        original_bg = btn.cget('bg')
        
        # Flash animation
        btn.config(bg=self.colors['cell_safe_hint'])
        self.root.after(100, lambda: btn.config(bg=self.colors['cell_revealed']))
        self.update_button(r, c)
    
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
            self.buttons[r][c].config(text="", bg=self.colors['cell_unknown'])
        else:
            self.flags.add((r, c))
            self.stats.flags_placed += 1
            self.buttons[r][c].config(text="🚩", bg=self.colors['cell_flag'])
        
        self.update_mine_count()
    
    def update_button(self, r: int, c: int):
        """Update button appearance based on cell value."""
        value = self.board[r][c]
        btn = self.buttons[r][c]
        
        if value == 0:
            btn.config(text="", bg=self.colors['cell_revealed'], relief=tk.SUNKEN)
        elif isinstance(value, int) and value > 0:
            color = self.colors['numbers'][value - 1]
            btn.config(text=str(value), bg=self.colors['cell_revealed'], 
                      fg=color, relief=tk.SUNKEN)
    
    def reveal_all_mines(self):
        """Reveal all mines when game is over."""
        for r, c in self.mine_positions:
            self.buttons[r][c].config(text="💣", bg=self.colors['cell_mine'], 
                                     fg=self.colors['fg'], relief=tk.SUNKEN)
    
    def update_mine_count(self):
        """Update mine counter."""
        remaining = self.mines - len(self.flags)
        self.mine_label.config(text=f"💣 Mines: {remaining}")
    
    def update_timer(self):
        """Update game timer."""
        if self.timer_running and self.game_start_time:
            elapsed = int(datetime.now().timestamp() - self.game_start_time)
            self.time_label.config(text=f"⏱️ Time: {elapsed}s")
        
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
        self.create_enhanced_board()
        self.game_start_time = None
        self.timer_running = False
        self.auto_solving = False
        self.update_mine_count()
        self.time_label.config(text="⏱️ Time: 0s")
        self.status_label.config(text="🎮 Ready to play!")
        self.progress_bar.pack_forget()
        self.logger.info("New game started")
    
    def change_difficulty(self, event=None):
        """Change game difficulty."""
        self.config.difficulty = self.difficulty_var.get()
        self.save_config()
        self.new_game()
    
    def change_theme(self, event=None):
        """Change UI theme."""
        self.config.theme = self.theme_var.get()
        self.save_config()
        self.apply_theme()
        self.create_enhanced_board()
    
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
    
    def start_auto_solve(self):
        """Start automatic solving in a separate thread."""
        if self.auto_solving:
            return
        
        if self.first_click:
            messagebox.showinfo("Auto-Solve", "Please make your first move to start the game!")
            return
        
        self.auto_solving = True
        self.status_label.config(text="🤖 Auto-solving...")
        self.progress_bar.pack(side=tk.LEFT, padx=10)
        self.progress_var.set(0)
        
        # Start auto-solve in separate thread
        thread = threading.Thread(target=self.auto_solve_worker)
        thread.daemon = True
        thread.start()
    
    def auto_solve_worker(self):
        """Worker thread for auto-solving."""
        try:
            mines, safe, probs = self.get_ai_suggestions()
            
            # Calculate progress
            total_cells = self.rows * self.cols
            revealed_target = total_cells - self.mines
            progress_steps = 0
            
            speed_map = {
                "Slow": 1.0,
                "Medium": 0.5,
                "Fast": 0.2,
                "Instant": 0.05
            }
            delay = speed_map.get(self.speed_var.get(), 0.5)
            
            while self.auto_solving and not self.game_over and not self.game_won:
                # Apply certain mines
                for r, c in list(mines):
                    if not self.auto_solving:
                        break
                    if self.board[r][c] == -1:
                        self.root.after(0, lambda rr=r, cc=c: self.toggle_flag(rr, cc))
                        time.sleep(delay)
                        mines.remove((r, c))
                
                # Apply safe cells
                for r, c in list(safe):
                    if not self.auto_solving:
                        break
                    if self.board[r][c] == -1:
                        self.root.after(0, lambda rr=r, cc=c: self.reveal_cell(rr, cc, animate=True))
                        time.sleep(delay)
                        safe.remove((r, c))
                        progress_steps += 1
                
                # Update progress
                progress = (self.revealed_count / revealed_target) * 100
                self.root.after(0, lambda p=progress: self.progress_var.set(p))
                
                # Get new suggestions
                mines, safe, probs = self.get_ai_suggestions()
                
                # If no certain moves, make a probability-based guess
                if not mines and not safe and probs:
                    best_cell = min(probs.items(), key=lambda x: x[1])
                    r, c = best_cell[0]
                    if self.board[r][c] == -1:
                        self.root.after(0, lambda rr=r, cc=c: self.reveal_cell(rr, cc, animate=True))
                        time.sleep(delay)
                        progress_steps += 1
                
                # Check if we should stop
                if self.game_over or self.game_won:
                    break
                
                # Safety check to avoid infinite loops
                if progress_steps > 100:
                    break
            
            # Clean up
            self.root.after(0, self.finish_auto_solve)
            
        except Exception as e:
            self.logger.error(f"Auto-solve error: {e}")
            self.root.after(0, self.finish_auto_solve)
    
    def finish_auto_solve(self):
        """Finish auto-solving and clean up."""
        self.auto_solving = False
        self.progress_bar.pack_forget()
        
        if self.game_won:
            self.stats.auto_solves_completed += 1
            self.status_label.config(text="🎉 Auto-solve Complete! 🎉")
        elif self.game_over:
            self.status_label.config(text="💥 Auto-solve Failed! 💥")
        else:
            self.status_label.config(text="🤖 Auto-solve Stopped")
        
        if self.config.auto_save:
            self.save_stats()
    
    def show_ai_hints(self):
        """Show enhanced AI hints dialog."""
        mines, safe, probs = self.get_ai_suggestions()
        
        dialog = tk.Toplevel(self.root)
        dialog.title("🤖 AI Analysis")
        dialog.geometry("450x400")
        dialog.configure(bg=self.colors['bg'])
        
        # Title
        title_frame = ttk.Frame(dialog)
        title_frame.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Label(title_frame, text="🤖 AI Analysis", font=('Arial', 14, 'bold')).pack()
        
        # Results frame
        results_frame = ttk.LabelFrame(dialog, text="Analysis Results", padding=10)
        results_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Label(results_frame, text=f"Certain Mines: {len(mines)}", font=('Arial', 10)).pack(anchor=tk.W, pady=2)
        ttk.Label(results_frame, text=f"Safe Cells: {len(safe)}", font=('Arial', 10)).pack(anchor=tk.W, pady=2)
        ttk.Label(results_frame, text=f"Probability Calculations: {len(probs)}", font=('Arial', 10)).pack(anchor=tk.W, pady=2)
        
        # Button frame
        button_frame = ttk.Frame(dialog)
        button_frame.pack(fill=tk.X, padx=10, pady=10)
        
        if mines or safe:
            def apply_hints():
                for r, c in mines:
                    if self.board[r][c] == -1:
                        self.toggle_flag(r, c)
                for r, c in safe:
                    if self.board[r][c] == -1:
                        self.reveal_cell(r, c, animate=True)
                dialog.destroy()
            
            ttk.Button(button_frame, text="✅ Apply Hints", command=apply_hints).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(button_frame, text="❌ Close", command=dialog.destroy).pack(side=tk.RIGHT, padx=5)
    
    def show_stats(self):
        """Show enhanced statistics dialog."""
        dialog = tk.Toplevel(self.root)
        dialog.title("📊 Statistics")
        dialog.geometry("350x300")
        dialog.configure(bg=self.colors['bg'])
        
        # Title
        ttk.Label(dialog, text="📊 Game Statistics", font=('Arial', 14, 'bold')).pack(pady=10)
        
        # Stats frame
        stats_frame = ttk.LabelFrame(dialog, text="Performance Metrics", padding=15)
        stats_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        stats_data = [
            ("Games Played:", f"{self.stats.games_played}"),
            ("Games Won:", f"{self.stats.games_won}"),
            ("Win Rate:", f"{self.stats.win_rate:.1f}%"),
            ("Best Time:", f"{self.stats.best_time:.1f}s" if self.stats.best_time != float('inf') else "N/A"),
            ("Average Time:", f"{self.stats.total_time / self.stats.games_played:.1f}s" if self.stats.games_played > 0 else "N/A"),
            ("AI Suggestions Used:", f"{self.stats.ai_suggestions_used}"),
            ("Auto-Solves Completed:", f"{self.stats.auto_solves_completed}"),
            ("Total Flags Placed:", f"{self.stats.flags_placed}"),
        ]
        
        for label, value in stats_data:
            frame = ttk.Frame(stats_frame)
            frame.pack(fill=tk.X, pady=2)
            ttk.Label(frame, text=label, font=('Arial', 10)).pack(side=tk.LEFT)
            ttk.Label(frame, text=value, font=('Arial', 10, 'bold')).pack(side=tk.RIGHT)
        
        ttk.Button(dialog, text="Close", command=dialog.destroy).pack(pady=10)
    
    def show_settings(self):
        """Show enhanced settings dialog."""
        dialog = tk.Toplevel(self.root)
        dialog.title("⚙️ Settings")
        dialog.geometry("300x250")
        dialog.configure(bg=self.colors['bg'])
        
        # Title
        ttk.Label(dialog, text="⚙️ Settings", font=('Arial', 14, 'bold')).pack(pady=10)
        
        # Settings frame
        settings_frame = ttk.LabelFrame(dialog, text="Game Options", padding=15)
        settings_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # AI enabled
        ai_var = tk.BooleanVar(value=self.config.ai_enabled)
        ttk.Checkbutton(settings_frame, text="🤖 AI Assistant", variable=ai_var,
                       command=lambda: self.update_setting('ai_enabled', ai_var.get())).pack(anchor=tk.W, pady=5)
        
        # Auto save
        save_var = tk.BooleanVar(value=self.config.auto_save)
        ttk.Checkbutton(settings_frame, text="💾 Auto-save Statistics", variable=save_var,
                       command=lambda: self.update_setting('auto_save', save_var.get())).pack(anchor=tk.W, pady=5)
        
        ttk.Button(dialog, text="Close", command=dialog.destroy).pack(pady=10)
    
    def update_setting(self, key: str, value: Any):
        """Update a setting."""
        setattr(self.config, key, value)
        self.save_config()
    
    def run(self):
        """Start the enhanced GUI application."""
        try:
            self.logger.info("Enhanced GUI Minesweeper started")
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
        game = EnhancedMinesweeperGUI()
        game.run()
    except Exception as e:
        print(f"Failed to start enhanced GUI game: {e}")
        messagebox.showerror("Error", f"Failed to start game: {e}")


if __name__ == "__main__":
    main()
