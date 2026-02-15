#!/usr/bin/env python3
"""
Cyberpunk Minesweeper - Complete Integration
Combines the Neural UI System with Minesweeper AI for the ultimate cyberpunk experience
"""

import tkinter as tk
from tkinter import ttk, messagebox
import random
import json
import time
import math
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
    auto_save: bool = True
    theme: str = "cyberpunk"
    risk_level: float = 0.5


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


class CyberpunkUI:
    """Cyberpunk-styled UI system for Minesweeper."""
    
    # Cyberpunk color palette
    COLORS = {
        'bg': '#0a0a0a',
        'fg': '#00ffcc',
        'cell_unknown': '#1a1a2e',
        'cell_revealed': '#0f0f1e',
        'cell_mine': '#ff0040',
        'cell_flag': '#ffaa00',
        'cell_safe_hint': '#00ff88',
        'cell_mine_hint': '#ff4400',
        'button_bg': '#16213e',
        'button_fg': '#00ffcc',
        'button_hover': '#0f3460',
        'button_active': '#00ffcc',
        'text_primary': '#00ffcc',
        'text_secondary': '#8892b0',
        'text_danger': '#ff0040',
        'text_success': '#00ff88',
        'text_warning': '#ffaa00',
        'accent_cyan': '#00ffcc',
        'accent_green': '#00ff88',
        'accent_orange': '#ffaa00',
        'accent_red': '#ff0040',
        'accent_purple': '#cc00ff',
        'numbers': [
            '#00ffcc',  # 1 - cyan
            '#00ff88',  # 2 - green
            '#ffaa00',  # 3 - orange
            '#cc00ff',  # 4 - purple
            '#ff0040',  # 5 - red
            '#ff0088',  # 6 - pink
            '#ffffff',  # 7 - white
            '#8892b0',  # 8 - gray
        ]
    }
    
    def __init__(self, root):
        self.root = root
        self.root.configure(bg=self.COLORS['bg'])
        self.root.title("🤖 CYBERPUNK MINESWEEPER AI")
        
        # UI elements
        self.buttons = []
        self.logic_feed = []
        self.animation_time = 0
        
        # Fonts
        self.font_mono = ('Consolas', 10)
        self.font_header = ('Consolas', 12, 'bold')
        self.font_title = ('Consolas', 16, 'bold')
        
    def create_cyberpunk_button(self, parent, text, command, width=12):
        """Create a cyberpunk-styled button."""
        btn = tk.Button(
            parent,
            text=text,
            command=command,
            width=width,
            bg=self.COLORS['button_bg'],
            fg=self.COLORS['button_fg'],
            font=self.font_mono,
            relief=tk.FLAT,
            bd=2,
            cursor='hand2'
        )
        
        # Add hover effects
        def on_enter(e):
            btn.config(bg=self.COLORS['button_hover'])
        
        def on_leave(e):
            btn.config(bg=self.COLORS['button_bg'])
        
        btn.bind('<Enter>', on_enter)
        btn.bind('<Leave>', on_leave)
        
        return btn
    
    def create_cyberpunk_frame(self, parent, text):
        """Create a cyberpunk-styled frame."""
        frame = ttk.LabelFrame(
            parent,
            text=text,
            padding=10,
            labelanchor='n'
        )
        
        # Style the frame
        style = ttk.Style()
        style.theme_use('clam')
        style.configure(
            'Cyber.TLabelframe',
            background=self.COLORS['bg'],
            foreground=self.COLORS['accent_cyan'],
            bordercolor=self.COLORS['accent_cyan'],
            lightcolor=self.COLORS['accent_cyan'],
            darkcolor=self.COLORS['accent_cyan']
        )
        style.configure(
            'Cyber.TLabelframe.Label',
            background=self.COLORS['bg'],
            foreground=self.COLORS['accent_cyan'],
            font=self.font_header
        )
        
        frame.configure(style='Cyber.TLabelframe')
        return frame
    
    def add_logic_entry(self, message, entry_type="INFO"):
        """Add entry to the logic feed."""
        timestamp = datetime.now().strftime("%H:%M:%S")
        formatted_message = f"[{entry_type}] {message}"
        
        self.logic_feed.append({
            'text': formatted_message,
            'type': entry_type,
            'timestamp': timestamp
        })
        
        # Keep only recent entries
        if len(self.logic_feed) > 15:
            self.logic_feed.pop(0)
    
    def get_entry_color(self, entry_type):
        """Get color for logic entry type."""
        colors = {
            "SOLVE": self.COLORS['accent_green'],
            "LOGIC": self.COLORS['accent_cyan'],
            "PROB": self.COLORS['accent_orange'],
            "FOGIC": self.COLORS['accent_purple'],
            "ERROR": self.COLORS['accent_red'],
            "INFO": self.COLORS['text_secondary']
        }
        return colors.get(entry_type, self.COLORS['text_secondary'])
    
    def create_probability_cell(self, parent, r, c, prob=0.0, callback=None):
        """Create a probability cell with cyberpunk styling."""
        # Calculate color based on probability
        if prob < 0.1:
            bg_color = self.COLORS['cell_safe_hint']
            text_color = self.COLORS['accent_green']
        elif prob < 0.3:
            bg_color = '#00ff44'
            text_color = self.COLORS['bg']
        elif prob < 0.6:
            bg_color = self.COLORS['accent_orange']
            text_color = self.COLORS['bg']
        elif prob < 0.8:
            bg_color = '#ff4400'
            text_color = self.COLORS['fg']
        else:
            bg_color = self.COLORS['cell_mine_hint']
            text_color = self.COLORS['text_danger']
        
        btn = tk.Button(
            parent,
            text=f"{int(prob*100)}%" if prob > 0 and prob < 1 else "",
            bg=bg_color,
            fg=text_color,
            font=self.font_mono,
            relief=tk.FLAT,
            bd=1,
            width=4,
            height=2,
            cursor='hand2'
        )
        
        if callback:
            btn.bind('<Button-1>', lambda e: callback(r, c))
        
        return btn
    
    def update_animation(self):
        """Update animation timers."""
        self.animation_time += 0.1


class CyberpunkMinesweeper:
    """Main Cyberpunk Minesweeper game with AI integration."""
    
    DIFFICULTY_PRESETS = {
        "beginner": {"rows": 8, "cols": 8, "mines": 10},
        "easy": {"rows": 10, "cols": 10, "mines": 15},
        "medium": {"rows": 12, "cols": 12, "mines": 25},
        "hard": {"rows": 16, "cols": 16, "mines": 40},
        "expert": {"rows": 20, "cols": 20, "mines": 80}
    }
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.geometry("1000x700")
        self.root.resizable(False, False)
        
        # Initialize UI
        self.ui = CyberpunkUI(self.root)
        
        # Game state
        self.config = self.load_config()
        self.stats = self.load_stats()
        self.setup_game()
        
        # Game variables
        self.game_start_time = None
        self.timer_running = False
        self.auto_solving = False
        
        # Create GUI
        self.create_cyberpunk_gui()
        
        # Start animations
        self.update_timer()
        self.update_animations()
        # throttle logic feed updates
        self._last_feed_update = 0.0
        
    def load_config(self) -> GameConfig:
        """Load configuration from file."""
        config_file = Path.home() / ".cyberpunk_minesweeper" / "config.json"
        
        try:
            if config_file.exists():
                with open(config_file, 'r') as f:
                    data = json.load(f)
                return GameConfig(**data)
        except Exception:
            pass
        
        return GameConfig()
    
    def save_config(self):
        """Save configuration to file."""
        config_file = Path.home() / ".cyberpunk_minesweeper" / "config.json"
        config_file.parent.mkdir(exist_ok=True)
        
        try:
            with open(config_file, 'w') as f:
                json.dump(asdict(self.config), f, indent=2)
        except Exception:
            pass
    
    def load_stats(self) -> GameStats:
        """Load statistics from file."""
        stats_file = Path.home() / ".cyberpunk_minesweeper" / "stats.json"
        
        try:
            if stats_file.exists():
                with open(stats_file, 'r') as f:
                    data = json.load(f)
                return GameStats(**data)
        except Exception:
            pass
        
        return GameStats()
    
    def save_stats(self):
        """Save statistics to file."""
        stats_file = Path.home() / ".cyberpunk_minesweeper" / "stats.json"
        stats_file.parent.mkdir(exist_ok=True)
        
        try:
            if self.stats.games_played > 0:
                self.stats.win_rate = (self.stats.games_won / self.stats.games_played) * 100
            
            with open(stats_file, 'w') as f:
                json.dump(asdict(self.stats), f, indent=2)
        except Exception:
            pass
    
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
        self.probabilities = {}
        
        self.ui.add_logic_entry(f"Board initialized: {self.rows}x{self.cols} with {self.mines} mines", "LOGIC")
    
    def create_cyberpunk_gui(self):
        """Create the cyberpunk GUI interface."""
        # Main container
        main_frame = tk.Frame(self.root, bg=self.ui.COLORS['bg'])
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Title
        title_label = tk.Label(
            main_frame,
            text="🤖 CYBERPUNK MINESWEEPER AI",
            font=self.ui.font_title,
            bg=self.ui.COLORS['bg'],
            fg=self.ui.COLORS['accent_cyan']
        )
        title_label.pack(pady=(0, 10))
        
        # Top control panel
        top_frame = self.ui.create_cyberpunk_frame(main_frame, "🎮 NEURAL CONTROLS")
        top_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Difficulty selector
        difficulty_frame = tk.Frame(top_frame, bg=self.ui.COLORS['bg'])
        difficulty_frame.pack(side=tk.LEFT, padx=5)
        
        tk.Label(
            difficulty_frame,
            text="DIFFICULTY:",
            font=self.ui.font_mono,
            bg=self.ui.COLORS['bg'],
            fg=self.ui.COLORS['text_secondary']
        ).pack(side=tk.LEFT, padx=5)
        
        self.difficulty_var = tk.StringVar(value=self.config.difficulty)
        difficulty_menu = ttk.Combobox(
            difficulty_frame,
            textvariable=self.difficulty_var,
            values=list(self.DIFFICULTY_PRESETS.keys()),
            state="readonly",
            width=12,
            font=self.ui.font_mono
        )
        difficulty_menu.pack(side=tk.LEFT, padx=5)
        difficulty_menu.bind('<<ComboboxSelected>>', self.change_difficulty)
        
        # Control buttons
        self.new_game_btn = self.ui.create_cyberpunk_button(
            top_frame, "🔄 NEW GAME", self.new_game
        )
        self.new_game_btn.pack(side=tk.LEFT, padx=5)
        
        self.ai_solve_btn = self.ui.create_cyberpunk_button(
            top_frame, "🤖 AI SOLVE", self.start_auto_solve
        )
        self.ai_solve_btn.pack(side=tk.LEFT, padx=5)
        
        self.hints_btn = self.ui.create_cyberpunk_button(
            top_frame, "💡 HINTS", self.show_ai_hints
        )
        self.hints_btn.pack(side=tk.LEFT, padx=5)
        
        # Status panel
        status_frame = tk.Frame(top_frame, bg=self.ui.COLORS['bg'])
        status_frame.pack(side=tk.RIGHT, padx=10)
        
        self.mine_label = tk.Label(
            status_frame,
            text=f"💣 MINES: {self.mines}",
            font=self.ui.font_mono,
            bg=self.ui.COLORS['bg'],
            fg=self.ui.COLORS['accent_orange']
        )
        self.mine_label.pack(side=tk.LEFT, padx=10)
        
        self.time_label = tk.Label(
            status_frame,
            text="⏱️ TIME: 0s",
            font=self.ui.font_mono,
            bg=self.ui.COLORS['bg'],
            fg=self.ui.COLORS['accent_cyan']
        )
        self.time_label.pack(side=tk.LEFT, padx=10)
        
        self.status_label = tk.Label(
            status_frame,
            text="🎮 READY",
            font=self.ui.font_mono,
            bg=self.ui.COLORS['bg'],
            fg=self.ui.COLORS['accent_green']
        )
        self.status_label.pack(side=tk.LEFT, padx=10)
        
        # Middle section with game board and logic feed
        middle_frame = tk.Frame(main_frame, bg=self.ui.COLORS['bg'])
        middle_frame.pack(fill=tk.BOTH, expand=True)
        
        # Game board
        board_frame = self.ui.create_cyberpunk_frame(middle_frame, "🎯 NEURAL GRID")
        board_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        self.create_game_board(board_frame)
        
        # Logic feed
        logic_frame = self.ui.create_cyberpunk_frame(middle_frame, "📜 LOGIC FEED")
        logic_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        self.create_logic_feed(logic_frame)
        
        # Bottom panel with risk slider
        bottom_frame = self.ui.create_cyberpunk_frame(main_frame, "⚡ RISK MANAGEMENT")
        bottom_frame.pack(fill=tk.X, pady=(10, 0))
        
        self.create_risk_slider(bottom_frame)
    
    def create_game_board(self, parent):
        """Create the game board."""
        # Board container
        board_container = tk.Frame(parent, bg=self.ui.COLORS['bg'])
        board_container.pack(padx=10, pady=10)
        
        self.buttons = []
        
        for r in range(self.rows):
            button_row = []
            for c in range(self.cols):
                btn = tk.Button(
                    board_container,
                    text="",
                    bg=self.ui.COLORS['cell_unknown'],
                    fg=self.ui.COLORS['text_primary'],
                    font=self.ui.font_mono,
                    relief=tk.FLAT,
                    bd=1,
                    width=3,
                    height=1,
                    cursor='hand2'
                )
                btn.grid(row=r, column=c, padx=1, pady=1)
                btn.bind('<Button-1>', lambda e, row=r, col=c: self.left_click(row, col))
                btn.bind('<Button-3>', lambda e, row=r, col=c: self.right_click(row, col))
                
                # Add hover effects
                def on_enter(e, b=btn):
                    if b.cget('bg') == self.ui.COLORS['cell_unknown']:
                        b.config(bg=self.ui.COLORS['button_hover'])
                
                def on_leave(e, b=btn):
                    if b.cget('bg') == self.ui.COLORS['button_hover']:
                        b.config(bg=self.ui.COLORS['cell_unknown'])
                
                btn.bind('<Enter>', on_enter)
                btn.bind('<Leave>', on_leave)
                
                button_row.append(btn)
            self.buttons.append(button_row)
    
    def create_logic_feed(self, parent):
        """Create the logic feed display."""
        # Feed container
        feed_container = tk.Frame(parent, bg=self.ui.COLORS['bg'])
        feed_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Text widget with scrollbar
        text_frame = tk.Frame(feed_container, bg=self.ui.COLORS['bg'])
        text_frame.pack(fill=tk.BOTH, expand=True)
        
        self.logic_text = tk.Text(
            text_frame,
            width=30,
            height=20,
            bg=self.ui.COLORS['cell_revealed'],
            fg=self.ui.COLORS['text_primary'],
            font=self.ui.font_mono,
            relief=tk.FLAT,
            bd=0,
            wrap=tk.WORD
        )
        
        scrollbar = tk.Scrollbar(text_frame, command=self.logic_text.yview)
        self.logic_text.config(yscrollcommand=scrollbar.set)
        
        self.logic_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Initial entry
        self.ui.add_logic_entry("Neural system initialized", "LOGIC")
        self.ui.add_logic_entry("AI ready for analysis", "SOLVE")
        self.update_logic_feed()
    
    def create_risk_slider(self, parent):
        """Create the risk management slider."""
        slider_container = tk.Frame(parent, bg=self.ui.COLORS['bg'])
        slider_container.pack(fill=tk.X, padx=10, pady=10)
        
        # Risk label
        tk.Label(
            slider_container,
            text="RISK LEVEL:",
            font=self.ui.font_mono,
            bg=self.ui.COLORS['bg'],
            fg=self.ui.COLORS['text_secondary']
        ).pack(side=tk.LEFT, padx=10)
        
        # Risk slider
        self.risk_var = tk.DoubleVar(value=self.config.risk_level)
        risk_slider = tk.Scale(
            slider_container,
            from_=0.0,
            to=1.0,
            orient=tk.HORIZONTAL,
            variable=self.risk_var,
            resolution=0.1,
            length=300,
            bg=self.ui.COLORS['button_bg'],
            fg=self.ui.COLORS['accent_cyan'],
            troughcolor=self.ui.COLORS['cell_revealed'],
            activebackground=self.ui.COLORS['accent_cyan'],
            highlightthickness=0,
            command=self.update_risk_level
        )
        risk_slider.pack(side=tk.LEFT, padx=10)
        
        # Risk labels
        self.risk_label = tk.Label(
            slider_container,
            text="BALANCED",
            font=self.ui.font_mono,
            bg=self.ui.COLORS['bg'],
            fg=self.ui.COLORS['accent_cyan']
        )
        self.risk_label.pack(side=tk.LEFT, padx=10)
    
    def update_risk_level(self, value):
        """Update risk level."""
        self.config.risk_level = float(value)
        self.save_config()
        
        # Update risk label
        if self.config.risk_level < 0.3:
            risk_text = "CONSERVATIVE"
            color = self.ui.COLORS['accent_green']
        elif self.config.risk_level < 0.7:
            risk_text = "BALANCED"
            color = self.ui.COLORS['accent_cyan']
        else:
            risk_text = "AGGRESSIVE"
            color = self.ui.COLORS['accent_red']
        
        self.risk_label.config(text=risk_text, fg=color)
        self.ui.add_logic_entry(f"Risk level set to {risk_text} ({self.config.risk_level:.1f})", "LOGIC")
    
    def update_logic_feed(self):
        """Update the logic feed display (throttled)."""
        now = time.time()
        if now - getattr(self, '_last_feed_update', 0.0) < 0.5:
            return
        self._last_feed_update = now

        self.logic_text.delete(1.0, tk.END)

        for entry in self.ui.logic_feed:
            color = self.ui.get_entry_color(entry['type'])
            self.logic_text.insert(tk.END, f"{entry['text']}\n")

            # Apply color to the last line
            line_start = f"{self.logic_text.index('end-2c')} linestart"
            line_end = f"{self.logic_text.index('end-2c')} lineend"
            self.logic_text.tag_add(entry['type'], line_start, line_end)
            self.logic_text.tag_config(entry['type'], foreground=color)

        self.logic_text.see(tk.END)
    
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
            self.ui.add_logic_entry(f"Mines placed: {len(self.mine_positions)} positions", "LOGIC")
        except ValueError:
            self.ui.add_logic_entry("Failed to place mines - invalid configuration", "ERROR")
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
            self.game_start_time = time.time()
            self.timer_running = True
            self.ui.add_logic_entry("Game started - neural analysis initiated", "LOGIC")
        
        self.reveal_cell(r, c)
    
    def right_click(self, r: int, c: int, event=None):
        """Handle right click on cell."""
        if self.game_over or self.game_won or self.auto_solving:
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
                self.ui.add_logic_entry(f"💥 MINE DETONATED at ({r}, {c})", "ERROR")
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
                self.ui.add_logic_entry("🎉 BOARD CLEARED - VICTORY!", "SOLVE")
            
        except Exception as e:
            self.ui.add_logic_entry(f"Error revealing cell ({r}, {c}): {e}", "ERROR")
    
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
            self.buttons[r][c].config(text="", bg=self.ui.COLORS['cell_unknown'])
            self.ui.add_logic_entry(f"Flag removed from ({r}, {c})", "LOGIC")
        else:
            self.flags.add((r, c))
            self.stats.flags_placed += 1
            self.buttons[r][c].config(text="🚩", bg=self.ui.COLORS['cell_flag'])
            self.ui.add_logic_entry(f"Flag placed at ({r}, {c})", "LOGIC")
        
        self.update_mine_count()
    
    def update_button(self, r: int, c: int):
        """Update button appearance based on cell value."""
        value = self.board[r][c]
        btn = self.buttons[r][c]
        
        if value == 0:
            btn.config(text="", bg=self.ui.COLORS['cell_revealed'], relief=tk.SUNKEN)
        elif isinstance(value, int) and value > 0:
            color = self.ui.COLORS['numbers'][value - 1]
            btn.config(text=str(value), bg=self.ui.COLORS['cell_revealed'], 
                      fg=color, relief=tk.SUNKEN)
    
    def reveal_all_mines(self):
        """Reveal all mines when game is over."""
        for r, c in self.mine_positions:
            self.buttons[r][c].config(text="💣", bg=self.ui.COLORS['cell_mine'], 
                                     fg=self.ui.COLORS['text_danger'], relief=tk.SUNKEN)
    
    def update_mine_count(self):
        """Update mine counter."""
        remaining = self.mines - len(self.flags)
        self.mine_label.config(text=f"💣 MINES: {remaining}")
    
    def update_timer(self):
        """Update game timer."""
        if self.timer_running and self.game_start_time:
            elapsed = int(time.time() - self.game_start_time)
            self.time_label.config(text=f"⏱️ TIME: {elapsed}s")
        
        self.root.after(1000, self.update_timer)
    
    def update_animations(self):
        """Update animations."""
        self.ui.update_animation()
        self.update_logic_feed()
        self.root.after(100, self.update_animations)
    
    def end_game(self, won: bool):
        """Handle game end."""
        if self.game_start_time:
            game_time = time.time() - self.game_start_time
            self.stats.total_time += game_time
            
            if won and (self.stats.best_time == float('inf') or game_time < self.stats.best_time):
                self.stats.best_time = game_time
        
        self.stats.games_played += 1
        if won:
            self.stats.games_won += 1
            self.stats.mines_cleared += len(self.mine_positions)
            self.status_label.config(text="🎉 VICTORY!", fg=self.ui.COLORS['accent_green'])
        else:
            self.status_label.config(text="💥 GAME OVER", fg=self.ui.COLORS['text_danger'])
        
        if self.config.auto_save:
            self.save_stats()
    
    def new_game(self):
        """Start a new game."""
        self.setup_game()
        self.create_game_board(self.root.winfo_children()[0].winfo_children()[1].winfo_children()[0])
        self.game_start_time = None
        self.timer_running = False
        self.auto_solving = False
        self.update_mine_count()
        self.time_label.config(text="⏱️ TIME: 0s")
        self.status_label.config(text="🎮 READY", fg=self.ui.COLORS['accent_green'])
        self.ui.add_logic_entry("New game initialized", "LOGIC")
    
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
            self.ui.add_logic_entry(f"AI analysis: {len(mines)} mines, {len(safe)} safe cells", "PROB")
            
            return mines, safe, probs
            
        except Exception as e:
            self.ui.add_logic_entry(f"AI analysis failed: {e}", "ERROR")
            return set(), set(), {}
    
    def start_auto_solve(self):
        """Start automatic solving."""
        if self.auto_solving:
            return
        
        if self.first_click:
            self.ui.add_logic_entry("Make first move before auto-solving", "LOGIC")
            return
        
        self.auto_solving = True
        self.status_label.config(text="🤖 AUTO-SOLVING", fg=self.ui.COLORS['accent_cyan'])
        self.ui.add_logic_entry("Neural auto-solver activated", "SOLVE")
        
        self.auto_solve_worker()
    
    def auto_solve_worker(self):
        """Worker for auto-solving."""
        try:
            mines, safe, probs = self.get_ai_suggestions()
            # Build a sequence of scheduled actions (non-blocking)
            actions = []
            delay_ms = 0
            STEP_DELAY = 400

            # Schedule flagging mines
            for r, c in list(mines):
                if not self.auto_solving:
                    break
                if self.board[r][c] == -1:
                    actions.append((delay_ms, self.toggle_flag, (r, c)))
                    delay_ms += STEP_DELAY

            # Schedule revealing safe cells
            for r, c in list(safe):
                if not self.auto_solving:
                    break
                if self.board[r][c] == -1:
                    actions.append((delay_ms, self.reveal_cell, (r, c)))
                    delay_ms += STEP_DELAY

            # If no certain moves, schedule probability-based guess
            if not mines and not safe and probs:
                best_cell = min(probs.items(), key=lambda x: x[1])
                r, c = best_cell[0]
                if self.board[r][c] == -1:
                    actions.append((delay_ms, self.reveal_cell, (r, c)))
                    self.ui.add_logic_entry(f"Probability guess at ({r}, {c}) - {best_cell[1]:.3f}", "PROB")
                    delay_ms += STEP_DELAY

            # Schedule the actions using root.after
            for ms, func, args in actions:
                self.root.after(ms, lambda f=func, a=args: f(*a))

            # Continue after scheduled sequence completes
            finish_delay = max(500, delay_ms + 200)
            if not self.game_over and not self.game_won and self.auto_solving:
                self.root.after(finish_delay, self.auto_solve_worker)
            else:
                self.root.after(finish_delay, self.finish_auto_solve)
                
        except Exception as e:
            self.ui.add_logic_entry(f"Auto-solve error: {e}", "ERROR")
            self.finish_auto_solve()
    
    def finish_auto_solve(self):
        """Finish auto-solving."""
        self.auto_solving = False
        if self.game_won:
            self.stats.auto_solves_completed += 1
            self.status_label.config(text="🎉 AUTO-SOLVE COMPLETE", fg=self.ui.COLORS['accent_green'])
        elif self.game_over:
            self.status_label.config(text="💥 AUTO-SOLVE FAILED", fg=self.ui.COLORS['text_danger'])
        else:
            self.status_label.config(text="🎮 READY", fg=self.ui.COLORS['accent_green'])
        
        if self.config.auto_save:
            self.save_stats()
    
    def show_ai_hints(self):
        """Show AI hints dialog."""
        mines, safe, probs = self.get_ai_suggestions()
        
        # Create hints window
        hints_window = tk.Toplevel(self.root)
        hints_window.title("🤖 NEURAL ANALYSIS")
        hints_window.geometry("400x300")
        hints_window.configure(bg=self.ui.COLORS['bg'])
        
        # Title
        tk.Label(
            hints_window,
            text="🤖 NEURAL ANALYSIS RESULTS",
            font=self.ui.font_title,
            bg=self.ui.COLORS['bg'],
            fg=self.ui.COLORS['accent_cyan']
        ).pack(pady=10)
        
        # Results
        results_text = f"""
Certain Mines: {len(mines)}
Safe Cells: {len(safe)}
Probability Calculations: {len(probs)}

Risk Level: {self.config.risk_level:.1f}
AI Suggestions Used: {self.stats.ai_suggestions_used}
        """
        
        tk.Label(
            hints_window,
            text=results_text,
            font=self.ui.font_mono,
            bg=self.ui.COLORS['bg'],
            fg=self.ui.COLORS['text_primary'],
            justify=tk.LEFT
        ).pack(pady=10)
        
        # Apply hints button
        if mines or safe:
            def apply_hints():
                for r, c in mines:
                    if self.board[r][c] == -1:
                        self.toggle_flag(r, c)
                for r, c in safe:
                    if self.board[r][c] == -1:
                        self.reveal_cell(r, c)
                hints_window.destroy()
            
            self.ui.create_cyberpunk_button(
                hints_window, "✅ APPLY HINTS", apply_hints
            ).pack(pady=10)
        
        # Close button
        self.ui.create_cyberpunk_button(
            hints_window, "❌ CLOSE", hints_window.destroy
        ).pack(pady=5)
    
    def run(self):
        """Run the game."""
        try:
            self.ui.add_logic_entry("Cyberpunk Minesweeper AI initialized", "LOGIC")
            self.ui.add_logic_entry("Neural systems online", "SOLVE")
            self.root.mainloop()
        except Exception as e:
            self.ui.add_logic_entry(f"Fatal error: {e}", "ERROR")
        finally:
            self.save_config()
            self.save_stats()


def main():
    """Main entry point."""
    try:
        game = CyberpunkMinesweeper()
        game.run()
    except Exception as e:
        messagebox.showerror("Error", f"Failed to start game: {e}")


if __name__ == "__main__":
    main()
