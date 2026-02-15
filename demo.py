#!/usr/bin/env python3
"""
AI Minesweeper Demo 🕵️‍♂️💣

This demo showcases the different AI solving techniques:
1. Basic logical deduction
2. Constraint satisfaction 
3. Probability-based guessing
4. Interactive GUI with AI assistance

Run this file to see all the AI capabilities in action!
"""

from minesweeper_ai import MinesweeperAI, MinesweeperGame
from advanced_solver import AdvancedMinesweeperAI
import time
import random


def demo_basic_solver():
    """Demonstrate basic logical deduction."""
    print("🎯 DEMO 1: Basic Logical Deduction")
    print("=" * 60)
    
    # A board where basic logic can solve everything
    board = [
        [1, -1, -1, 1],
        [2,  2,  2, 1],
        [-1, 2, -1, -1],
        [1,  1,  1, 1]
    ]
    
    print("Initial board:")
    for row in board:
        print(' '.join(str(cell).rjust(3) for cell in row))
    print()
    
    ai = MinesweeperAI(board)
    mines, safe = ai.solve()
    
    print("\nFinal board:")
    ai.print_board()
    
    print(f"✅ Basic solver found {len(mines)} mines and {len(safe)} safe cells")
    input("\nPress Enter to continue...")


def demo_constraint_satisfaction():
    """Demonstrate constraint satisfaction solving."""
    print("\n🔗 DEMO 2: Constraint Satisfaction")
    print("=" * 60)
    
    # A board that requires constraint analysis
    board = [
        [ 1, -1, -1,  1],
        [-1,  2,  2, -1],
        [-1,  2, -1, -1],
        [ 1, -1, -1,  1]
    ]
    
    print("Initial board (requires constraint analysis):")
    for row in board:
        print(' '.join(str(cell).rjust(3) for cell in row))
    print()
    
    ai = AdvancedMinesweeperAI(board)
    mines, safe, probs = ai.solve()
    
    print("\nFinal board:")
    ai.print_board()
    
    print(f"✅ Advanced solver found {len(mines)} mines and {len(safe)} safe cells")
    if probs:
        print(f"📊 Calculated probabilities for {len(probs)} cells")
    
    input("\nPress Enter to continue...")


def demo_probability_guessing():
    """Demonstrate probability-based guessing."""
    print("\n🎲 DEMO 3: Probability-Based Guessing")
    print("=" * 60)
    
    # Classic ambiguous pattern - only probability can help
    board = [
        [1, -1, -1],
        [-1, 2, -1],
        [-1, -1, 1]
    ]
    
    print("Initial board (classic ambiguous pattern):")
    for row in board:
        print(' '.join(str(cell).rjust(3) for cell in row))
    print()
    
    ai = AdvancedMinesweeperAI(board)
    mines, safe, probs = ai.solve()
    
    print("\nFinal board:")
    ai.print_board()
    
    print("📊 Mine Probabilities:")
    for cell, prob in sorted(probs.items()):
        status = "💣 MINE" if prob > 0.5 else "✅ SAFE" if prob < 0.5 else "❓ UNKNOWN"
        print(f"  ({cell[0]},{cell[1]}): {prob:.3f} {status}")
    
    best_guess = ai.get_best_guess()
    if best_guess:
        print(f"\n🎯 AI's safest guess: ({best_guess[0]},{best_guess[1]}) with {probs[best_guess]:.3f} mine probability")
    
    input("\nPress Enter to continue...")


def demo_random_game():
    """Demonstrate AI on a randomly generated game."""
    print("\n🎰 DEMO 4: Random Game Challenge")
    print("=" * 60)
    
    # Create a challenging random game
    game = MinesweeperGame(8, 8, 12)
    game.place_mines()
    game.calculate_numbers()
    
    # Reveal some cells to give AI something to work with
    player_board = game.get_player_board()
    
    # Smart reveal: reveal cells that create interesting patterns
    safe_cells = [(r, c) for r in range(8) for c in range(8) 
                  if game.board[r][c] != 'M']
    
    # Reveal a strategic pattern
    reveal_pattern = [
        (1, 1), (1, 2), (1, 3),
        (2, 1), (2, 3),
        (3, 1), (3, 2), (3, 3)
    ]
    
    revealed_count = 0
    for r, c in reveal_pattern:
        if (r, c) in safe_cells and revealed_count < 8:
            player_board[r][c] = game.board[r][c]
            revealed_count += 1
    
    print(f"Partially revealed 8x8 board with 12 mines:")
    for row in player_board:
        print(' '.join(str(cell).rjust(3) for cell in row))
    print()
    
    # Run basic solver first
    print("🔍 Running basic solver...")
    basic_ai = MinesweeperAI([row[:] for row in player_board])
    basic_mines, basic_safe = basic_ai.solve()
    
    # Then run advanced solver
    print("\n🧠 Running advanced solver...")
    advanced_ai = AdvancedMinesweeperAI(player_board)
    adv_mines, adv_safe, probs = advanced_ai.solve()
    
    # Check accuracy
    actual_mines = game.mine_positions
    basic_correct = len(basic_mines.intersection(actual_mines))
    adv_correct = len(adv_mines.intersection(actual_mines))
    
    print(f"\n📊 Performance Comparison:")
    print(f"  Basic AI: {basic_correct}/{len(actual_mines)} mines correct")
    print(f"  Advanced AI: {adv_correct}/{len(actual_mines)} mines correct")
    print(f"  Improvement: +{adv_correct - basic_correct} mines")
    
    input("\nPress Enter to continue...")


def demo_performance_test():
    """Performance test on multiple random games."""
    print("\n⚡ DEMO 5: Performance Test")
    print("=" * 60)
    
    games_won = 0
    total_games = 10
    total_mines_found = 0
    total_actual_mines = 0
    
    for i in range(total_games):
        print(f"Testing game {i+1}/{total_games}...", end=" ")
        
        # Create game
        game = MinesweeperGame(6, 6, 8)
        game.place_mines()
        game.calculate_numbers()
        
        # Reveal some cells
        player_board = game.get_player_board()
        safe_cells = [(r, c) for r in range(6) for c in range(6) 
                      if game.board[r][c] != 'M']
        
        if len(safe_cells) > 6:
            revealed = random.sample(safe_cells, 6)
            for r, c in revealed:
                player_board[r][c] = game.board[r][c]
        
        # Run AI
        ai = AdvancedMinesweeperAI(player_board)
        mines, safe, probs = ai.solve()
        
        # Check if won (all mines found)
        actual_mines = game.mine_positions
        mines_correct = len(mines.intersection(actual_mines))
        
        total_mines_found += mines_correct
        total_actual_mines += len(actual_mines)
        
        if mines_correct == len(actual_mines):
            games_won += 1
            print("✅ WON")
        else:
            print(f"❌ {mines_correct}/{len(actual_mines)} mines")
    
    accuracy = (total_mines_found / total_actual_mines) * 100
    win_rate = (games_won / total_games) * 100
    
    print(f"\n🏆 Performance Summary:")
    print(f"  Games won: {games_won}/{total_games} ({win_rate:.1f}%)")
    print(f"  Mine accuracy: {total_mines_found}/{total_actual_mines} ({accuracy:.1f}%)")
    
    input("\nPress Enter to continue...")


def main():
    """Run all demos."""
    print("🤖 AI Minesweeper Demo Suite")
    print("=" * 60)
    print("This demo showcases different AI solving techniques.")
    print("Each demo will pause for you to review the results.\n")
    
    demos = [
        demo_basic_solver,
        demo_constraint_satisfaction,
        demo_probability_guessing,
        demo_random_game,
        demo_performance_test
    ]
    
    for demo in demos:
        try:
            demo()
        except KeyboardInterrupt:
            print("\n\nDemo interrupted by user.")
            break
        except Exception as e:
            print(f"\n❌ Demo failed with error: {e}")
            continue
    
    print("\n🎉 Demo Complete!")
    print("\nTo try the interactive GUI:")
    print("  python gui_minesweeper.py")
    print("\nGUI Controls:")
    print("  Left Click: Reveal cell")
    print("  Right Click: Flag/unflag cell")
    print("  AI Solve Button: Run AI analysis")
    print("  Toggle Hints Button: Show/hide AI suggestions")
    print("  New Game Button: Start fresh game")
    print("  Spacebar: Apply AI hints")
    print("  N key: New game")


if __name__ == "__main__":
    main()
