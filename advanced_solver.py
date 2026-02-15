from itertools import product, combinations
from typing import List, Tuple, Set, Dict
import random
from collections import defaultdict


class AdvancedMinesweeperAI:
    """Advanced AI with constraint satisfaction and probability reasoning."""
    
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
        self.probabilities = {}
        # caches to speed up repeated neighbour lookups
        self._neighbor_cache = {}

    def get_neighbors(self, r: int, c: int) -> List[Tuple[int, int]]:
        """Get all valid neighboring cells."""
        key = (r, c)
        if key in self._neighbor_cache:
            return self._neighbor_cache[key]

        neighbors = []
        for dr, dc in product([-1, 0, 1], repeat=2):
            if dr == 0 and dc == 0:
                continue
            nr, nc = r + dr, c + dc
            if 0 <= nr < self.rows and 0 <= nc < self.cols:
                neighbors.append((nr, nc))

        self._neighbor_cache[key] = neighbors
        return neighbors

    def basic_logical_step(self) -> bool:
        """Perform basic logical deduction (Rules 1 & 2)."""
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

                    # Rule 1: All unknown are safe
                    if flagged == number and unknown:
                        for ur, uc in unknown:
                            if self.board[ur][uc] == -1:
                                print(f"Safe (Rule 1): ({ur},{uc})")
                                self.board[ur][uc] = 0
                                self.safe_cells.add((ur, uc))
                                changed = True

                    # Rule 2: All unknown are mines
                    elif len(unknown) + flagged == number and unknown:
                        for ur, uc in unknown:
                            if self.board[ur][uc] == -1:
                                print(f"Mine (Rule 2): ({ur},{uc})")
                                self.board[ur][uc] = 'F'
                                self.mines_found.add((ur, uc))
                                changed = True

        return changed

    def get_constraint_variables(self) -> Dict[Tuple[int, int], List[Tuple[int, int]]]:
        """Get all constraint variables (unknown cells adjacent to numbered cells)."""
        constraints = {}
        
        for r in range(self.rows):
            for c in range(self.cols):
                if isinstance(self.board[r][c], int) and self.board[r][c] > 0:
                    neighbors = self.get_neighbors(r, c)
                    unknown_neighbors = []
                    flagged = 0
                    
                    for nr, nc in neighbors:
                        if self.board[nr][nc] == -1:
                            unknown_neighbors.append((nr, nc))
                        elif self.board[nr][nc] == 'F':
                            flagged += 1
                    
                    if unknown_neighbors:
                        # Store: (r,c) -> [(unknown_neighbors), remaining_mines_needed]
                        constraints[(r, c)] = (unknown_neighbors, self.board[r][c] - flagged)
        
        return constraints

    def constraint_satisfaction_step(self) -> bool:
        """Advanced constraint satisfaction using subset analysis."""
        constraints = self.get_constraint_variables()
        changed = False

        if not constraints:
            return False

        # Find all unknown cells involved in constraints
        all_unknown = set()
        for (r, c), (unknown_neighbors, _) in constraints.items():
            all_unknown.update(unknown_neighbors)

        # Try to find deterministic solutions through constraint analysis
        for cell1 in constraints:
            unknown1, mines1 = constraints[cell1]
            
            for cell2 in constraints:
                if cell1 >= cell2:  # Avoid duplicates and self-comparison
                    continue
                    
                unknown2, mines2 = constraints[cell2]
                
                # Check if unknown1 is a subset of unknown2
                set1, set2 = set(unknown1), set(unknown2)
                
                if set1.issubset(set2):
                    # unknown1 ⊂ unknown2: mines2 - mines1 mines in unknown2\unknown1
                    diff_cells = set2 - set1
                    diff_mines = mines2 - mines1
                    
                    if diff_mines == 0 and diff_cells:
                        # All diff_cells are safe
                        for ur, uc in diff_cells:
                            if self.board[ur][uc] == -1:
                                print(f"Safe (Subset): ({ur},{uc})")
                                self.board[ur][uc] = 0
                                self.safe_cells.add((ur, uc))
                                changed = True
                    
                    elif len(diff_cells) == diff_mines and diff_cells:
                        # All diff_cells are mines
                        for ur, uc in diff_cells:
                            if self.board[ur][uc] == -1:
                                print(f"Mine (Subset): ({ur},{uc})")
                                self.board[ur][uc] = 'F'
                                self.mines_found.add((ur, uc))
                                changed = True

        return changed

    def calculate_probabilities(self) -> Dict[Tuple[int, int], float]:
        """Calculate mine probabilities for all unknown cells."""
        constraints = self.get_constraint_variables()
        
        if not constraints:
            return {}

        # Get all unknown cells involved in constraints
        all_unknown = set()
        for (r, c), (unknown_neighbors, _) in constraints.items():
            all_unknown.update(unknown_neighbors)

        if not all_unknown:
            return {}

        unknown_list = list(all_unknown)

        # If the search space is small, enumerate exactly. If it's large, use Monte Carlo sampling to approximate.
        MAX_EXACT = 15
        probabilities = {cell: 0.0 for cell in unknown_list}

        if len(unknown_list) <= MAX_EXACT:
            valid_configurations = []
            # Try all possible mine counts (0 to len(unknown_list))
            for mine_count in range(len(unknown_list) + 1):
                for mine_positions in combinations(unknown_list, mine_count):
                    # Check if this configuration satisfies all constraints
                    valid = True
                    for (r, c), (unknown_neighbors, required_mines) in constraints.items():
                        mines_in_constraint = sum(1 for pos in mine_positions if pos in unknown_neighbors)
                        if mines_in_constraint != required_mines:
                            valid = False
                            break
                    if valid:
                        valid_configurations.append(set(mine_positions))

            if not valid_configurations:
                return {}

            total_configs = len(valid_configurations)
            for config in valid_configurations:
                for cell in config:
                    probabilities[cell] += 1.0 / total_configs

            self.probabilities = probabilities
            return probabilities

        # Monte Carlo approximation for large unknown sets
        SAMPLE_LIMIT = 3000
        samples = 0
        rng = random.Random()

        # Precompute required_mines mapping for faster checking
        constraint_list = [(set(unknowns), req) for unknowns, req in constraints.values()]

        attempts = 0
        while samples < SAMPLE_LIMIT and attempts < SAMPLE_LIMIT * 10:
            attempts += 1
            # Randomly choose a subset size roughly centered on expected mines
            pick = set()
            for cell in unknown_list:
                if rng.random() < 0.15:
                    pick.add(cell)

            # Validate config against constraints
            ok = True
            for unknowns_set, req in constraint_list:
                mines_in = len(unknowns_set & pick)
                if mines_in != req:
                    ok = False
                    break

            if ok:
                samples += 1
                for cell in pick:
                    probabilities[cell] += 1.0

        if samples == 0:
            return {}

        # Normalize
        for cell in probabilities:
            probabilities[cell] /= samples

        self.probabilities = probabilities
        return probabilities

    def get_best_guess(self) -> Tuple[int, int]:
        """Get the safest cell to guess based on probabilities."""
        if not self.probabilities:
            # Calculate probabilities if not done yet
            self.calculate_probabilities()
        
        if not self.probabilities:
            # No constraints, pick random unknown
            unknown_cells = [(r, c) for r in range(self.rows) for c in range(self.cols) 
                           if self.board[r][c] == -1]
            if unknown_cells:
                return random.choice(unknown_cells)
            return None

        # Find cell with lowest mine probability
        safest_cell = min(self.probabilities.keys(), key=lambda x: self.probabilities[x])
        return safest_cell

    def solve(self, use_probabilities: bool = True):
        """Run the complete solver with all techniques."""
        print("🧠 Starting Advanced AI Solver...")
        step = 0
        
        # Phase 1: Basic logical deduction
        print("📐 Phase 1: Basic logical deduction")
        while self.basic_logical_step():
            step += 1
            print(f"  Step {step} completed")
        
        # Phase 2: Constraint satisfaction
        print("🔗 Phase 2: Constraint satisfaction")
        constraint_steps = 0
        while self.constraint_satisfaction_step():
            constraint_steps += 1
            print(f"  Constraint step {constraint_steps} completed")
            # Try basic logic again after each constraint step
            while self.basic_logical_step():
                step += 1
                print(f"  Basic logic step {step} completed")
        
        # Phase 3: Probability calculation
        if use_probabilities:
            print("📊 Phase 3: Probability analysis")
            probabilities = self.calculate_probabilities()
            if probabilities:
                print("  Mine probabilities calculated:")
                for cell, prob in sorted(probabilities.items()):
                    if prob > 0:
                        print(f"    ({cell[0]},{cell[1]}): {prob:.3f}")
                
                best_guess = self.get_best_guess()
                if best_guess:
                    print(f"  🎯 Best guess: ({best_guess[0]},{best_guess[1]}) with {probabilities[best_guess]:.3f} mine probability")
        
        print(f"✅ Advanced solving complete. Found {len(self.mines_found)} mines, {len(self.safe_cells)} safe cells.")
        
        return self.mines_found, self.safe_cells, self.probabilities

    def print_board(self):
        """Print the current board state."""
        print("\nCurrent Board:")
        for row in self.board:
            print(' '.join(str(cell).rjust(2) for cell in row))
        print()


def test_advanced_solver():
    """Test the advanced solver on a complex scenario."""
    print("🧪 Testing Advanced Solver")
    print("=" * 50)
    
    # A more complex board that requires constraint satisfaction
    board = [
        [ 1, -1, -1,  1],
        [-1,  2,  2, -1],
        [-1,  2, -1, -1],
        [ 1, -1, -1,  1]
    ]
    
    print("Initial board:")
    for row in board:
        print(' '.join(str(cell).rjust(2) for cell in row))
    print()
    
    ai = AdvancedMinesweeperAI(board)
    mines, safe, probs = ai.solve()
    
    print("\nFinal board:")
    ai.print_board()
    
    print(f"🎯 Results: {len(mines)} mines found, {len(safe)} safe cells identified")
    if probs:
        print(f"📊 Probabilities calculated for {len(probs)} cells")


def test_probability_scenario():
    """Test a scenario where only probability-based guessing can help."""
    print("\n🎲 Testing Probability-Based Scenario")
    print("=" * 50)
    
    # This is a classic ambiguous pattern
    board = [
        [ 1, -1, -1],
        [-1,  2, -1],
        [-1, -1,  1]
    ]
    
    print("Initial board (ambiguous pattern):")
    for row in board:
        print(' '.join(str(cell).rjust(2) for cell in row))
    print()
    
    ai = AdvancedMinesweeperAI(board)
    mines, safe, probs = ai.solve()
    
    print("\nFinal board:")
    ai.print_board()
    
    print(f"🎯 Results: {len(mines)} mines found, {len(safe)} safe cells identified")
    if probs:
        print("📊 Mine probabilities:")
        for cell, prob in sorted(probs.items()):
            print(f"  ({cell[0]},{cell[1]}): {prob:.3f}")


if __name__ == "__main__":
    test_advanced_solver()
    test_probability_scenario()
