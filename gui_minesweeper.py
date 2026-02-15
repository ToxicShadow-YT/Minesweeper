import pygame
import sys
import random
from typing import List, Tuple, Optional
from advanced_solver import AdvancedMinesweeperAI


class MinesweeperGUI:
    """Interactive Minesweeper with AI assistant."""
    
    # Colors
    COLORS = {
        'background': (189, 189, 189),
        'cell_unknown': (189, 189, 189),
        'cell_revealed': (229, 229, 229),
        'cell_mine': (255, 0, 0),
        'cell_flag': (255, 0, 0),
        'cell_safe_hint': (0, 255, 0),
        'cell_mine_hint': (255, 165, 0),
        'border': (123, 123, 123),
        'border_raised': (255, 255, 255),
        'border_lowered': (123, 123, 123),
        'text': (0, 0, 0),
        'numbers': [
            (0, 0, 255),      # 1 - blue
            (0, 128, 0),      # 2 - green
            (255, 0, 0),      # 3 - red
            (0, 0, 128),      # 4 - dark blue
            (128, 0, 0),      # 5 - dark red
            (0, 128, 128),    # 6 - cyan
            (0, 0, 0),        # 7 - black
            (128, 128, 128),  # 8 - gray
        ]
    }
    
    def __init__(self, rows: int = 10, cols: int = 10, mines: int = 15):
        pygame.init()
        
        self.rows = rows
        self.cols = cols
        self.mines = mines
        self.cell_size = 30
        self.margin = 5
        
        # Calculate window size
        self.width = cols * self.cell_size + 2 * self.margin
        self.height = rows * self.cell_size + 2 * self.margin + 60  # Extra space for controls
        
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("AI Minesweeper 🤖💣")
        
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 20)
        self.small_font = pygame.font.Font(None, 16)
        
        # Game state
        self.board = [[-1 for _ in range(cols)] for _ in range(rows)]
        self.mine_positions = set()
        self.game_over = False
        self.game_won = False
        self.first_click = True
        
        # AI state
        self.ai = None
        self.ai_hints = {'safe': set(), 'mines': set()}
        self.show_ai_hints = False
        
        # UI elements
        self.ai_button = pygame.Rect(10, self.height - 50, 100, 30)
        self.hint_button = pygame.Rect(120, self.height - 50, 100, 30)
        self.new_game_button = pygame.Rect(230, self.height - 50, 100, 30)
        
        self.place_mines()
        self.calculate_numbers()
    
    def place_mines(self):
        """Place mines randomly."""
        positions = [(r, c) for r in range(self.rows) for c in range(self.cols)]
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
                    for dr in [-1, 0, 1]:
                        for dc in [-1, 0, 1]:
                            if dr == 0 and dc == 0:
                                continue
                            nr, nc = r + dr, c + dc
                            if 0 <= nr < self.rows and 0 <= nc < self.cols:
                                if self.internal_board[nr][nc] == -1:
                                    count += 1
                    self.internal_board[r][c] = count
    
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
            self.board[r][c] = 'F'
        elif self.board[r][c] == 'F':
            self.board[r][c] = -1
    
    def run_ai_solver(self):
        """Run the AI solver to get hints."""
        # Create a copy of the board for the AI
        ai_board = [row[:] for row in self.board]
        
        # Convert flags to 'F' for AI
        for r in range(self.rows):
            for c in range(self.cols):
                if ai_board[r][c] == 'F':
                    continue  # Keep as is
        
        self.ai = AdvancedMinesweeperAI(ai_board)
        mines, safe, probs = self.ai.solve()
        
        self.ai_hints['mines'] = mines
        self.ai_hints['safe'] = safe
        
        print(f"AI found {len(mines)} mines and {len(safe)} safe cells")
    
    def apply_ai_hints(self):
        """Apply AI hints to the board."""
        # Flag mines
        for r, c in self.ai_hints['mines']:
            if self.board[r][c] == -1:
                self.board[r][c] = 'F'
        
        # Reveal safe cells
        for r, c in self.ai_hints['safe']:
            if self.board[r][c] == -1:
                self.reveal_cell(r, c)
    
    def new_game(self):
        """Start a new game."""
        self.board = [[-1 for _ in range(self.cols)] for _ in range(self.rows)]
        self.game_over = False
        self.game_won = False
        self.first_click = True
        self.ai = None
        self.ai_hints = {'safe': set(), 'mines': set()}
        self.place_mines()
        self.calculate_numbers()
    
    def draw_cell(self, r: int, c: int):
        """Draw a single cell."""
        x = self.margin + c * self.cell_size
        y = self.margin + r * self.cell_size
        
        cell_value = self.board[r][c]
        
        # Determine cell color
        if cell_value == -1:  # Unknown
            color = self.COLORS['cell_unknown']
            # Show AI hints if enabled
            if self.show_ai_hints:
                if (r, c) in self.ai_hints['safe']:
                    color = self.COLORS['cell_safe_hint']
                elif (r, c) in self.ai_hints['mines']:
                    color = self.COLORS['cell_mine_hint']
        elif cell_value == 'F':  # Flagged
            color = self.COLORS['cell_revealed']
        elif cell_value == 'M':  # Mine
            color = self.COLORS['cell_mine']
        else:  # Revealed number
            color = self.COLORS['cell_revealed']
        
        # Draw cell
        pygame.draw.rect(self.screen, color, (x, y, self.cell_size, self.cell_size))
        
        # Draw border
        if cell_value == -1:  # Raised border for unknown cells
            pygame.draw.line(self.screen, self.COLORS['border_raised'], 
                           (x, y), (x + self.cell_size, y), 2)
            pygame.draw.line(self.screen, self.COLORS['border_raised'], 
                           (x, y), (x, y + self.cell_size), 2)
            pygame.draw.line(self.screen, self.COLORS['border_lowered'], 
                           (x + self.cell_size, y), (x + self.cell_size, y + self.cell_size), 2)
            pygame.draw.line(self.screen, self.COLORS['border_lowered'], 
                           (x, y + self.cell_size), (x + self.cell_size, y + self.cell_size), 2)
        else:  # Lowered border for revealed cells
            pygame.draw.line(self.screen, self.COLORS['border_lowered'], 
                           (x, y), (x + self.cell_size, y), 2)
            pygame.draw.line(self.screen, self.COLORS['border_lowered'], 
                           (x, y), (x, y + self.cell_size), 2)
            pygame.draw.line(self.screen, self.COLORS['border_raised'], 
                           (x + self.cell_size, y), (x + self.cell_size, y + self.cell_size), 2)
            pygame.draw.line(self.screen, self.COLORS['border_raised'], 
                           (x, y + self.cell_size), (x + self.cell_size, y + self.cell_size), 2)
        
        # Draw content
        if cell_value == 'F':  # Flag
            # Draw flag
            points = [
                (x + self.cell_size//3, y + self.cell_size//3),
                (x + 2*self.cell_size//3, y + self.cell_size//2),
                (x + self.cell_size//3, y + 2*self.cell_size//3)
            ]
            pygame.draw.polygon(self.screen, self.COLORS['cell_flag'], points)
            pygame.draw.line(self.screen, self.COLORS['text'], 
                           (x + self.cell_size//3, y + self.cell_size//3),
                           (x + self.cell_size//3, y + 2*self.cell_size//3), 2)
        
        elif cell_value == 'M':  # Mine
            # Draw mine
            pygame.draw.circle(self.screen, self.COLORS['text'], 
                             (x + self.cell_size//2, y + self.cell_size//2), 
                             self.cell_size//4)
            # Draw spikes
            for angle in range(0, 360, 45):
                import math
                rad = math.radians(angle)
                x1 = x + self.cell_size//2 + int(self.cell_size//6 * math.cos(rad))
                y1 = y + self.cell_size//2 + int(self.cell_size//6 * math.sin(rad))
                x2 = x + self.cell_size//2 + int(self.cell_size//3 * math.cos(rad))
                y2 = y + self.cell_size//2 + int(self.cell_size//3 * math.sin(rad))
                pygame.draw.line(self.screen, self.COLORS['text'], (x1, y1), (x2, y2), 2)
        
        elif isinstance(cell_value, int) and cell_value > 0:  # Number
            text = self.font.render(str(cell_value), True, self.COLORS['numbers'][cell_value-1])
            text_rect = text.get_rect(center=(x + self.cell_size//2, y + self.cell_size//2))
            self.screen.blit(text, text_rect)
    
    def draw(self):
        """Draw the entire game."""
        self.screen.fill(self.COLORS['background'])
        
        # Draw cells
        for r in range(self.rows):
            for c in range(self.cols):
                self.draw_cell(r, c)
        
        # Draw buttons
        pygame.draw.rect(self.screen, (100, 200, 100), self.ai_button)
        ai_text = self.small_font.render("AI Solve", True, (255, 255, 255))
        ai_rect = ai_text.get_rect(center=self.ai_button.center)
        self.screen.blit(ai_text, ai_rect)
        
        pygame.draw.rect(self.screen, (100, 100, 200), self.hint_button)
        hint_text = self.small_font.render("Toggle Hints", True, (255, 255, 255))
        hint_rect = hint_text.get_rect(center=self.hint_button.center)
        self.screen.blit(hint_text, hint_rect)
        
        pygame.draw.rect(self.screen, (200, 100, 100), self.new_game_button)
        new_text = self.small_font.render("New Game", True, (255, 255, 255))
        new_rect = new_text.get_rect(center=self.new_game_button.center)
        self.screen.blit(new_text, new_rect)
        
        # Draw status
        if self.game_over:
            status_text = "GAME OVER! 💥"
            status_color = (255, 0, 0)
        elif self.game_won:
            status_text = "YOU WIN! 🎉"
            status_color = (0, 255, 0)
        else:
            mines_left = self.mines - sum(1 for r in range(self.rows) for c in range(self.cols) 
                                        if self.board[r][c] == 'F')
            status_text = f"Mines: {mines_left}"
            status_color = (0, 0, 0)
        
        status = self.font.render(status_text, True, status_color)
        status_rect = status.get_rect(center=(self.width // 2, self.height - 25))
        self.screen.blit(status, status_rect)
        
        pygame.display.flip()
    
    def handle_click(self, pos, button):
        """Handle mouse clicks."""
        x, y = pos
        
        # Check button clicks
        if self.ai_button.collidepoint(pos):
            self.run_ai_solver()
            return
        
        if self.hint_button.collidepoint(pos):
            self.show_ai_hints = not self.show_ai_hints
            return
        
        if self.new_game_button.collidepoint(pos):
            self.new_game()
            return
        
        # Check cell clicks
        if (self.margin <= x < self.width - self.margin and 
            self.margin <= y < self.height - 60 - self.margin):
            
            c = (x - self.margin) // self.cell_size
            r = (y - self.margin) // self.cell_size
            
            if 0 <= r < self.rows and 0 <= c < self.cols:
                if button == 1:  # Left click - reveal
                    if self.board[r][c] == -1:
                        self.reveal_cell(r, c)
                elif button == 3:  # Right click - flag
                    if self.board[r][c] in [-1, 'F']:
                        self.toggle_flag(r, c)
    
    def run(self):
        """Main game loop."""
        running = True
        
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if not self.game_over and not self.game_won:
                        self.handle_click(event.pos, event.button)
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE and self.ai:
                        # Apply AI hints with spacebar
                        self.apply_ai_hints()
                    elif event.key == pygame.K_n:
                        # New game with N key
                        self.new_game()
            
            self.draw()
            self.clock.tick(60)
        
        pygame.quit()
        sys.exit()


def main():
    """Main function to run the GUI."""
    game = MinesweeperGUI(rows=12, cols=12, mines=20)
    game.run()


if __name__ == "__main__":
    main()
