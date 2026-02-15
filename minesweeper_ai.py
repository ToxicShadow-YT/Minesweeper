from itertools import product
from typing import List, Tuple, Set
import random


class MinesweeperAI:
    def __init__(self, board: List[List]):
        """
        board: 2D list
        -1 = unknown
        0-8 = revealed numbers
        'F' = flagged mine
        """
        self.board = board
        self.rows = len(board)
        self.cols = len(board[0])
        self.mines_found = set()
        self.safe_cells = set()

    def get_neighbors(self, r: int, c: int) -> List[Tuple[int, int]]:
        """Get all valid neighboring cells."""
        neighbors = []
        for dr, dc in product([-1, 0, 1], repeat=2):
            if dr == 0 and dc == 0:
                continue
            nr, nc = r + dr, c + dc
            if 0 <= nr < self.rows and 0 <= nc < self.cols:
                neighbors.append((nr, nc))
        return neighbors

    def solve_step(self) -> bool:
        """Perform one step of logical deduction. Returns True if any changes were made."""
        changed = False

        for r in range(self.rows):
            for c in range(self.cols):
                if isinstance(self.board[r][c], int) and self.board[r][c] > 0:
                    neighbors = self.get_neighbors(r, c)
                    unknown = []
                    flagged = 0

                    for nr, nc in neighbors:
                        if self.board[nr][nc] == -1:
                            unknown.append((nr, nc))
                        elif self.board[nr][nc] == 'F':
                            flagged += 1

                    number = self.board[r][c]

                    # Rule 1: All unknown are safe (if we already found all mines)
                    if flagged == number and unknown:
                        for ur, uc in unknown:
                            if self.board[ur][uc] == -1:
                                print(f"Safe: ({ur},{uc})")
                                self.board[ur][uc] = 0  # Mark as safe (simulate reveal)
                                self.safe_cells.add((ur, uc))
                                changed = True

                    # Rule 2: All unknown are mines (if remaining unknown = remaining mines)
                    elif len(unknown) + flagged == number and unknown:
                        for ur, uc in unknown:
                            if self.board[ur][uc] == -1:
                                print(f"Mine: ({ur},{uc})")
                                self.board[ur][uc] = 'F'
                                self.mines_found.add((ur, uc))
                                changed = True

        return changed

    def solve(self):
        """Run the logical solver until no more deductions can be made."""
        print("🔍 Starting logical deduction...")
        step = 0
        while self.solve_step():
            step += 1
            print(f"Step {step} completed")
        
        print(f"✅ Logical deduction complete. Found {len(self.mines_found)} mines, {len(self.safe_cells)} safe cells.")
        print("No more logical moves available.")
        
        return self.mines_found, self.safe_cells

    def get_board_state(self) -> List[List]:
        """Return current board state."""
        return self.board

    def print_board(self):
        """Print the current board state."""
        print("\nCurrent Board:")
        for row in self.board:
            print(' '.join(str(cell).rjust(2) for cell in row))
        print()


class MinesweeperGame:
    """Game generator for testing the AI."""
    
    def __init__(self, rows: int, cols: int, mines: int):
        self.rows = rows
        self.cols = cols
        self.mines = mines
        self.board = [[-1 for _ in range(cols)] for _ in range(rows)]
        self.mine_positions = set()
        
    def place_mines(self, safe_row: int = None, safe_col: int = None):
        """Place mines randomly, avoiding the first clicked cell if specified."""
        positions = [(r, c) for r in range(self.rows) for c in range(self.cols)]
        if safe_row is not None and safe_col is not None:
            positions.remove((safe_row, safe_col))
        
        self.mine_positions = set(random.sample(positions, self.mines))
        
        for r, c in self.mine_positions:
            self.board[r][c] = 'M'  # Mark mines internally
    
    def calculate_numbers(self):
        """Calculate numbers for each cell."""
        for r in range(self.rows):
            for c in range(self.cols):
                if self.board[r][c] != 'M':
                    count = 0
                    for dr, dc in product([-1, 0, 1], repeat=2):
                        if dr == 0 and dc == 0:
                            continue
                        nr, nc = r + dr, c + dc
                        if 0 <= nr < self.rows and 0 <= nc < self.cols:
                            if self.board[nr][nc] == 'M':
                                count += 1
                    self.board[r][c] = count
    
    def reveal_cell(self, r: int, c: int) -> bool:
        """Reveal a cell and return True if it's safe, False if it's a mine."""
        if self.board[r][c] == 'M':
            return False
        return True
    
    def get_player_board(self) -> List[List]:
        """Get the board as seen by the player (with -1 for unknown)."""
        player_board = [[-1 for _ in range(self.cols)] for _ in range(self.rows)]
        return player_board


def test_basic_solver():
    """Test the basic solver with a simple example."""
    print("🧪 Testing Basic Solver")
    print("=" * 50)
    
    # Example board from the description
    board = [
        [1, -1, -1],
        [1,  2, -1],
        [0,  1, -1]
    ]
    
    print("Initial board:")
    for row in board:
        print(' '.join(str(cell).rjust(2) for cell in row))
    print()
    
    ai = MinesweeperAI(board)
    mines, safe = ai.solve()
    
    print("\nFinal board:")
    ai.print_board()
    
    print(f"🎯 Results: {len(mines)} mines found, {len(safe)} safe cells identified")


def test_random_game():
    """Test the solver on a randomly generated game."""
    print("\n🎲 Testing on Random Game")
    print("=" * 50)
    
    # Create a 5x5 game with 5 mines
    game = MinesweeperGame(5, 5, 5)
    game.place_mines()
    game.calculate_numbers()
    
    # Simulate revealing some cells to give the AI something to work with
    player_board = game.get_player_board()
    
    # Reveal a few safe cells randomly
    safe_cells = [(r, c) for r in range(5) for c in range(5) 
                  if game.board[r][c] != 'M']
    reveal_count = min(8, len(safe_cells))
    revealed = random.sample(safe_cells, reveal_count)
    
    for r, c in revealed:
        player_board[r][c] = game.board[r][c]
    
    print("Partially revealed board:")
    for row in player_board:
        print(' '.join(str(cell).rjust(2) for cell in row))
    print()
    
    ai = MinesweeperAI(player_board)
    mines, safe = ai.solve()
    
    print("\nFinal board:")
    ai.print_board()
    
    # Check accuracy
    actual_mines = game.mine_positions
    correct_mines = mines.intersection(actual_mines)
    print(f"🎯 Accuracy: {len(correct_mines)}/{len(actual_mines)} mines correctly identified")


if __name__ == "__main__":
    test_basic_solver()
    test_random_game()
