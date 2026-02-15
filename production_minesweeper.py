#!/usr/bin/env python3
"""
Production-Ready Minesweeper with AI Assistant
Professional version with error handling, logging, configuration, and statistics
"""

import os
import sys
import json
import logging
import random
import traceback
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
    color_enabled: bool = True
    sound_enabled: bool = False
    auto_save: bool = True
    log_level: str = "INFO"


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


class ProductionMinesweeper:
    """Production-ready Minesweeper with professional features."""
    
    DIFFICULTY_PRESETS = {
        "beginner": {"rows": 8, "cols": 8, "mines": 10},
        "easy": {"rows": 10, "cols": 10, "mines": 15},
        "medium": {"rows": 12, "cols": 12, "mines": 25},
        "hard": {"rows": 16, "cols": 16, "mines": 40},
        "expert": {"rows": 20, "cols": 20, "mines": 80}
    }
    
    def __init__(self):
        self.setup_logging()
        self.config = self.load_config()
        self.stats = self.load_stats()
        self.setup_game()
        self.game_start_time = None
        self.logger.info("Production Minesweeper initialized")
    
    def setup_logging(self):
        """Setup comprehensive logging system."""
        log_dir = Path.home() / ".minesweeper_ai"
        log_dir.mkdir(exist_ok=True)
        
        log_file = log_dir / f"minesweeper_{datetime.now().strftime('%Y%m%d')}.log"
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_file),
                logging.StreamHandler(sys.stdout)
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
            self.logger.info("Configuration saved")
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
            # Update win rate
            if self.stats.games_played > 0:
                self.stats.win_rate = (self.stats.games_won / self.stats.games_played) * 100
            
            with open(stats_file, 'w') as f:
                json.dump(asdict(self.stats), f, indent=2)
            self.logger.info("Statistics saved")
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
        
        self.logger.info(f"Game setup: {self.rows}x{self.cols} with {self.mines} mines")
    
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
    
    def reveal_cell(self, r: int, c: int) -> bool:
        """Reveal a cell and return True if safe, False if mine."""
        try:
            if self.board[r][c] != -1:
                return True
            
            if (r, c) in self.mine_positions:
                self.board[r][c] = 'M'
                self.game_over = True
                self.end_game(False)
                self.logger.info(f"Game over: Mine hit at ({r}, {c})")
                return False
            
            # Reveal the cell
            self.board[r][c] = self.internal_board[r][c]
            self.revealed_count += 1
            
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
                            self.revealed_count += 1
                            if self.internal_board[nr][nc] == 0:
                                to_reveal.append((nr, nc))
            
            # Check win condition
            total_cells = self.rows * self.cols
            if self.revealed_count == total_cells - self.mines:
                self.game_won = True
                self.end_game(True)
                self.logger.info("Game won!")
            
            return True
            
        except Exception as e:
            self.logger.error(f"Error revealing cell ({r}, {c}): {e}")
            return False
    
    def toggle_flag(self, r: int, c: int):
        """Toggle flag on a cell."""
        try:
            if self.board[r][c] == -1:
                if (r, c) in self.flags:
                    self.flags.remove((r, c))
                    self.logger.debug(f"Flag removed from ({r}, {c})")
                else:
                    self.flags.add((r, c))
                    self.stats.flags_placed += 1
                    self.logger.debug(f"Flag placed at ({r}, {c})")
        except Exception as e:
            self.logger.error(f"Error toggling flag at ({r}, {c}): {e}")
    
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
        
        if self.config.auto_save:
            self.save_stats()
        
        self.logger.info(f"Game ended: {'Won' if won else 'Lost'}")
    
    def get_colors(self):
        """Get color scheme based on configuration."""
        if not self.config.color_enabled:
            return {key: '' for key in ['reset', 'red', 'green', 'yellow', 'blue', 'magenta', 'cyan', 'white', 'bold']}
        
        return {
            'reset': '\033[0m',
            'red': '\033[91m',
            'green': '\033[92m',
            'yellow': '\033[93m',
            'blue': '\033[94m',
            'magenta': '\033[95m',
            'cyan': '\033[96m',
            'white': '\033[97m',
            'bold': '\033[1m',
        }
    
    def clear_screen(self):
        """Clear terminal screen."""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def draw_board(self, show_mines: bool = False):
        """Draw game board with professional formatting."""
        colors = self.get_colors()
        
        print(f"\n{colors['bold']}   MINESWEEPER AI - Production Edition{colors['reset']}")
        print(f"   Difficulty: {self.config.difficulty.upper()} | Mines: {self.mines - len(self.flags)} | Flags: {len(self.flags)}")
        
        if self.game_start_time:
            elapsed = datetime.now().timestamp() - self.game_start_time
            print(f"   Time: {elapsed:.1f}s")
        
        print()
        
        # Column headers
        print("   " + " ".join(f"{c:2}" for c in range(self.cols)))
        print("   " + "---" * self.cols)
        
        for r in range(self.rows):
            print(f"{r:2} |", end="")
            
            for c in range(self.cols):
                cell_value = self.board[r][c]
                
                if cell_value == -1:  # Unknown
                    if (r, c) in self.flags:
                        print(f"{colors['red']} F {colors['reset']}", end="")
                    else:
                        print(" . ", end="")
                
                elif cell_value == 'M':  # Mine
                    if show_mines or self.game_over:
                        print(f"{colors['red']}* {colors['reset']}", end="")
                    else:
                        print(" . ", end="")
                
                elif isinstance(cell_value, int):  # Number
                    if cell_value == 0:
                        print("   ", end="")
                    else:
                        number_colors = {
                            1: colors['blue'], 2: colors['green'], 3: colors['red'],
                            4: colors['magenta'], 5: colors['yellow'], 6: colors['cyan'],
                            7: colors['white'], 8: colors['white']
                        }
                        color = number_colors.get(cell_value, colors['white'])
                        print(f"{color}{cell_value:2} {colors['reset']}", end="")
            
            print("|")
        
        print("   " + "---" * self.cols)
    
    def show_stats(self):
        """Display comprehensive statistics."""
        colors = self.get_colors()
        
        print(f"\n{colors['bold']}{colors['cyan']}📊 GAME STATISTICS{colors['reset']}")
        print("=" * 40)
        print(f"Games Played: {self.stats.games_played}")
        print(f"Games Won: {self.stats.games_won}")
        print(f"Win Rate: {self.stats.win_rate:.1f}%")
        
        if self.stats.best_time != float('inf'):
            print(f"Best Time: {self.stats.best_time:.1f}s")
        
        if self.stats.games_played > 0:
            avg_time = self.stats.total_time / self.stats.games_played
            print(f"Average Time: {avg_time:.1f}s")
        
        print(f"Total Mines Cleared: {self.stats.mines_cleared}")
        print(f"Total Flags Placed: {self.stats.flags_placed}")
        print(f"AI Suggestions Used: {self.stats.ai_suggestions_used}")
    
    def show_menu(self):
        """Display main menu."""
        colors = self.get_colors()
        
        while True:
            self.clear_screen()
            print(f"{colors['bold']}{colors['cyan']}🎮 MINESWEEPER AI - Production Edition{colors['reset']}")
            print("=" * 50)
            print()
            print("1. New Game")
            print("2. Change Difficulty")
            print("3. View Statistics")
            print("4. Settings")
            print("5. Help")
            print("6. Exit")
            print()
            
            try:
                choice = input(f"{colors['bold']}Select option (1-6): {colors['reset']}").strip()
                
                if choice == '1':
                    self.setup_game()
                    self.play_game()
                elif choice == '2':
                    self.change_difficulty()
                elif choice == '3':
                    self.show_stats()
                    input(f"\n{colors['yellow']}Press Enter to continue...{colors['reset']}")
                elif choice == '4':
                    self.show_settings()
                elif choice == '5':
                    self.show_help()
                elif choice == '6':
                    self.save_config()
                    self.save_stats()
                    print(f"{colors['green']}Goodbye!{colors['reset']}")
                    return
                else:
                    print(f"{colors['red']}Invalid option!{colors['reset']}")
                    input(f"{colors['yellow']}Press Enter to continue...{colors['reset']}")
                    
            except KeyboardInterrupt:
                print(f"\n{colors['yellow']}Exiting...{colors['reset']}")
                return
            except Exception as e:
                self.logger.error(f"Menu error: {e}")
                print(f"{colors['red']}An error occurred!{colors['reset']}")
                input(f"{colors['yellow']}Press Enter to continue...{colors['reset']}")
    
    def change_difficulty(self):
        """Change game difficulty."""
        colors = self.get_colors()
        
        print(f"\n{colors['bold']}SELECT DIFFICULTY{colors['reset']}")
        print("=" * 30)
        
        for i, (name, preset) in enumerate(self.DIFFICULTY_PRESETS.items(), 1):
            print(f"{i}. {name.title()} ({preset['rows']}x{preset['cols']}, {preset['mines']} mines)")
        
        try:
            choice = int(input(f"\n{colors['bold']}Select difficulty (1-{len(self.DIFFICULTY_PRESETS)}): {colors['reset']}"))
            difficulties = list(self.DIFFICULTY_PRESETS.keys())
            
            if 1 <= choice <= len(difficulties):
                self.config.difficulty = difficulties[choice - 1]
                self.save_config()
                print(f"{colors['green']}Difficulty changed to {self.config.difficulty.title()}{colors['reset']}")
            else:
                print(f"{colors['red']}Invalid choice!{colors['reset']}")
                
        except (ValueError, KeyboardInterrupt):
            print(f"{colors['red']}Invalid input!{colors['reset']}")
        
        input(f"{colors['yellow']}Press Enter to continue...{colors['reset']}")
    
    def show_settings(self):
        """Display and modify settings."""
        colors = self.get_colors()
        
        while True:
            self.clear_screen()
            print(f"\n{colors['bold']}{colors['cyan']}⚙️ SETTINGS{colors['reset']}")
            print("=" * 30)
            print(f"1. AI Assistant: {'Enabled' if self.config.ai_enabled else 'Disabled'}")
            print(f"2. Colors: {'Enabled' if self.config.color_enabled else 'Disabled'}")
            print(f"3. Auto-save: {'Enabled' if self.config.auto_save else 'Disabled'}")
            print(f"4. Back to Menu")
            print()
            
            try:
                choice = input(f"{colors['bold']}Select option (1-4): {colors['reset']}").strip()
                
                if choice == '1':
                    self.config.ai_enabled = not self.config.ai_enabled
                    self.save_config()
                elif choice == '2':
                    self.config.color_enabled = not self.config.color_enabled
                    self.save_config()
                elif choice == '3':
                    self.config.auto_save = not self.config.auto_save
                    self.save_config()
                elif choice == '4':
                    break
                else:
                    print(f"{colors['red']}Invalid option!{colors['reset']}")
                    
            except KeyboardInterrupt:
                break
            
            input(f"{colors['yellow']}Press Enter to continue...{colors['reset']}")
    
    def show_help(self):
        """Display comprehensive help."""
        colors = self.get_colors()
        
        help_text = f"""
{colors['bold']}{colors['cyan']}🎮 MINESWEEPER AI - HELP{colors['reset']}
{'=' * 50}

{colors['bold']}GAMEPLAY:{colors['reset']}
• Reveal all cells without hitting mines to win
• Numbers show adjacent mine count
• Use flags to mark suspected mines
• AI assistant provides intelligent suggestions

{colors['bold']}COMMANDS:{colors['reset']}
• r row col  - Reveal cell at (row, col)
• c row col  - Clear cell (same as reveal)
• f row col  - Flag/unflag cell at (row, col)
• a          - Show AI suggestions
• s          - Show current statistics
• m          - Return to main menu
• q          - Quit current game

{colors['bold']}EXAMPLES:{colors['reset']}
• r 5 3     - Reveal cell at row 5, column 3
• f 2 7     - Flag cell at row 2, column 7
• a          - Get AI assistance

{colors['bold']}AI FEATURES:{colors['reset']}
• Basic logical deduction (Rules 1 & 2)
• Constraint satisfaction analysis
• Probability-based guessing
• Optimal move suggestions

{colors['bold']}LEGEND:{colors['reset']}
• .  - Unknown cell
• F  - Flagged mine
• *  - Mine (revealed)
• 1-8 - Number of adjacent mines

{colors['bold']}TIPS:{colors['reset']}
• Start with corners or edges
• Use AI suggestions when stuck
• Flag certain mines first
• Reveal safe cells immediately
"""
        
        print(help_text)
        input(f"{colors['yellow']}Press Enter to continue...{colors['reset']}")
    
    def play_game(self):
        """Main game loop."""
        self.game_start_time = datetime.now().timestamp()
        self.logger.info(f"Game started: {self.config.difficulty} difficulty")
        
        while not self.game_over and not self.game_won:
            self.clear_screen()
            self.draw_board()
            
            if self.game_over:
                print(f"\n{colors['red']}{colors['bold']}💥 GAME OVER! 💥{colors['reset']}")
                self.draw_board(show_mines=True)
                break
            
            if self.game_won:
                print(f"\n{colors['green']}{colors['bold']}🎉 YOU WIN! 🎉{colors['reset']}")
                self.draw_board(show_mines=True)
                break
            
            colors = self.get_colors()
            try:
                cmd = input(f"\n{colors['bold']}Command (r/c/f/a/s/m/q): {colors['reset']}").strip().lower()
                
                if cmd == 'q':
                    self.logger.info("Game quit by user")
                    break
                
                elif cmd == 'm':
                    return
                
                elif cmd == 's':
                    self.show_stats()
                    input(f"\n{colors['yellow']}Press Enter to continue...{colors['reset']}")
                
                elif cmd == 'a':
                    mines, safe, probs = self.get_ai_suggestions()
                    self.show_ai_hints(mines, safe, probs)
                    input(f"\n{colors['yellow']}Press Enter to continue...{colors['reset']}")
                
                else:
                    parts = cmd.split()
                    if len(parts) >= 3:
                        action = parts[0]
                        r = int(parts[1])
                        c = int(parts[2])
                        
                        if action in ['r', 'c'] and 0 <= r < self.rows and 0 <= c < self.cols:
                            if self.first_click:
                                self.place_mines(r, c)
                                self.calculate_numbers()
                                self.first_click = False
                            
                            self.reveal_cell(r, c)
                        
                        elif action == 'f' and 0 <= r < self.rows and 0 <= c < self.cols:
                            self.toggle_flag(r, c)
                        
                        else:
                            print(f"{colors['red']}Invalid input!{colors['reset']}")
                            input(f"{colors['yellow']}Press Enter to continue...{colors['reset']}")
                    else:
                        print(f"{colors['red']}Invalid format! Use: action row col{colors['reset']}")
                        input(f"{colors['yellow']}Press Enter to continue...{colors['reset']}")
            
            except (ValueError, IndexError):
                print(f"{colors['red']}Invalid input!{colors['reset']}")
                input(f"{colors['yellow']}Press Enter to continue...{colors['reset']}")
            except KeyboardInterrupt:
                print(f"\n{colors['yellow']}Returning to menu...{colors['reset']}")
                break
            except Exception as e:
                self.logger.error(f"Game error: {e}")
                print(f"{colors['red']}An error occurred!{colors['reset']}")
                input(f"{colors['yellow']}Press Enter to continue...{colors['reset']}")
    
    def show_ai_hints(self, mines, safe, probs):
        """Display AI hints."""
        colors = self.get_colors()
        
        print(f"\n{colors['cyan']}🤖 AI ANALYSIS{colors['reset']}")
        print("=" * 30)
        print(f"Mines found: {len(mines)}")
        print(f"Safe cells: {len(safe)}")
        
        if mines:
            print(f"\n{colors['red']}🚩 CERTAIN MINES:{colors['reset']}")
            for r, c in sorted(mines):
                print(f"  ({r}, {c})")
        
        if safe:
            print(f"\n{colors['green']}✅ SAFE CELLS:{colors['reset']}")
            for r, c in sorted(safe):
                print(f"  ({r}, {c})")
        
        if probs and not mines and not safe:
            print(f"\n{colors['yellow']}📊 BEST GUESSES:{colors['reset']}")
            sorted_probs = sorted(probs.items(), key=lambda x: x[1])[:5]
            for (r, c), prob in sorted_probs:
                status = "SAFE" if prob < 0.1 else "RISKY" if prob > 0.5 else "MODERATE"
                print(f"  ({r}, {c}): {prob:.3f} - {status}")
    
    def run(self):
        """Main application entry point."""
        try:
            self.logger.info("Production Minesweeper started")
            self.show_menu()
        except KeyboardInterrupt:
            print(f"\nExiting...")
        except Exception as e:
            self.logger.critical(f"Fatal error: {e}")
            self.logger.critical(traceback.format_exc())
            print(f"A critical error occurred. Check logs for details.")
        finally:
            self.save_config()
            self.save_stats()


def main():
    """Main entry point."""
    try:
        game = ProductionMinesweeper()
        game.run()
    except Exception as e:
        print(f"Failed to start game: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
