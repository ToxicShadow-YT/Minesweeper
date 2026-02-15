#!/usr/bin/env python3
"""
AI Trainer for Cyberpunk Minesweeper
Advanced training system to improve AI performance through machine learning
"""

import json
import time
import random
import statistics
from pathlib import Path
from typing import List, Dict, Tuple, Any
from dataclasses import dataclass, asdict
from advanced_solver import AdvancedMinesweeperAI
import numpy as np
import concurrent.futures
import os


@dataclass
class TrainingSession:
    """Training session data."""
    session_id: str
    timestamp: float
    board_size: Tuple[int, int]
    mine_count: int
    games_played: int
    games_won: int
    win_rate: float
    avg_solve_time: float
    best_solve_time: float
    accuracy_metrics: Dict[str, float]
    learning_data: List[Dict[str, Any]]


@dataclass
class AIModel:
    """AI model with learned parameters."""
    model_id: str
    version: str
    training_sessions: int
    total_games: int
    overall_win_rate: float
    learned_patterns: Dict[str, Any]
    probability_weights: Dict[str, float]
    strategy_parameters: Dict[str, float]
    performance_history: List[Dict[str, float]]


class CyberpunkAITrainer:
    """Advanced AI trainer for Minesweeper with machine learning capabilities."""
    
    def __init__(self):
        self.training_data_path = Path.home() / ".cyberpunk_minesweeper" / "ai_training"
        self.training_data_path.mkdir(parents=True, exist_ok=True)
        
        self.current_session = None
        self.ai_model = self.load_model()
        self.training_history = self.load_training_history()
        
        # Training parameters
        self.batch_size = 100
        self.learning_rate = 0.01
        self.convergence_threshold = 0.001
        
        print("🤖 Cyberpunk AI Trainer initialized")
        print(f"📚 Loaded model: {self.ai_model.model_id} v{self.ai_model.version}")
        print(f"📊 Training sessions: {self.ai_model.training_sessions}")
        print(f"🎯 Overall win rate: {self.ai_model.overall_win_rate:.1%}")
    
    def load_model(self) -> AIModel:
        """Load existing AI model or create new one."""
        model_file = self.training_data_path / "ai_model.json"
        
        if model_file.exists():
            try:
                with open(model_file, 'r') as f:
                    data = json.load(f)
                return AIModel(**data)
            except Exception as e:
                print(f"⚠️ Error loading model: {e}")
        
        # Create new model
        return AIModel(
            model_id="cyberpunk_ai_v1",
            version="1.0.0",
            training_sessions=0,
            total_games=0,
            overall_win_rate=0.0,
            learned_patterns={},
            probability_weights={
                "adjacent_mines": 1.0,
                "corner_penalty": 0.8,
                "edge_penalty": 0.9,
                "pattern_bonus": 1.2,
                "certainty_threshold": 0.95
            },
            strategy_parameters={
                "risk_tolerance": 0.5,
                "exploration_rate": 0.1,
                "convergence_speed": 0.05,
                "pattern_recognition": 0.7
            },
            performance_history=[]
        )
    
    def save_model(self):
        """Save AI model to file."""
        model_file = self.training_data_path / "ai_model.json"
        try:
            with open(model_file, 'w') as f:
                json.dump(asdict(self.ai_model), f, indent=2)
            print(f"✅ Model saved: {model_file}")
        except Exception as e:
            print(f"❌ Error saving model: {e}")
    
    def load_training_history(self) -> List[TrainingSession]:
        """Load training history."""
        history_file = self.training_data_path / "training_history.json"
        
        if history_file.exists():
            try:
                with open(history_file, 'r') as f:
                    data = json.load(f)
                return [TrainingSession(**session) for session in data]
            except Exception as e:
                print(f"⚠️ Error loading history: {e}")
        
        return []
    
    def save_training_history(self):
        """Save training history to file."""
        history_file = self.training_data_path / "training_history.json"
        try:
            data = [asdict(session) for session in self.training_history]
            with open(history_file, 'w') as f:
                json.dump(data, f, indent=2)
            print(f"✅ Training history saved: {len(self.training_history)} sessions")
        except Exception as e:
            print(f"❌ Error saving history: {e}")
    
    def start_training_session(self, board_size: Tuple[int, int], mine_count: int) -> str:
        """Start a new training session."""
        session_id = f"session_{int(time.time())}"
        
        self.current_session = TrainingSession(
            session_id=session_id,
            timestamp=time.time(),
            board_size=board_size,
            mine_count=mine_count,
            games_played=0,
            games_won=0,
            win_rate=0.0,
            avg_solve_time=0.0,
            best_solve_time=float('inf'),
            accuracy_metrics={},
            learning_data=[]
        )
        
        print(f"🚀 Started training session: {session_id}")
        print(f"📏 Board size: {board_size[0]}x{board_size[1]}, Mines: {mine_count}")
        
        return session_id
    
    def simulate_game(self, rows: int, cols: int, mines: int) -> Dict[str, Any]:
        """Simulate a single game and collect training data."""
        # Create board
        board = [[-1 for _ in range(cols)] for _ in range(rows)]
        mine_positions = set()
        
        # Place mines randomly
        positions = [(r, c) for r in range(rows) for c in range(cols)]
        mine_positions = set(random.sample(positions, mines))
        
        # Calculate numbers
        internal_board = [[0 for _ in range(cols)] for _ in range(rows)]
        for r, c in mine_positions:
            internal_board[r][c] = -1
        
        for r in range(rows):
            for c in range(cols):
                if internal_board[r][c] != -1:
                    count = 0
                    for dr in [-1, 0, 1]:
                        for dc in [-1, 0, 1]:
                            if dr == 0 and dc == 0:
                                continue
                            nr, nc = r + dr, c + dc
                            if 0 <= nr < rows and 0 <= nc < cols:
                                if (nr, nc) in mine_positions:
                                    count += 1
                    internal_board[r][c] = count
        
        # Simulate gameplay with AI
        start_time = time.time()
        moves = 0
        revealed = set()
        flags = set()
        game_won = False
        
        # Make first safe move
        safe_cells = [(r, c) for r in range(rows) for c in range(cols) 
                     if (r, c) not in mine_positions]
        if safe_cells:
            first_move = random.choice(safe_cells)
            revealed.add(first_move)
            moves += 1
        
        # Use AI solver
        ai = AdvancedMinesweeperAI(board)
        
        while len(revealed) < rows * cols - mines and moves < 1000:
            # Update AI board
            ai_board = [row[:] for row in board]
            for r, c in revealed:
                ai_board[r][c] = internal_board[r][c]
            for r, c in flags:
                if ai_board[r][c] == -1:
                    ai_board[r][c] = 'F'
            
            # Get AI suggestions
            ai = AdvancedMinesweeperAI(ai_board)
            mines_found, safe_cells_found, probabilities = ai.solve()
            
            # Apply AI suggestions
            move_made = False
            
            # Flag certain mines
            for r, c in mines_found:
                if (r, c) not in flags and (r, c) not in revealed:
                    flags.add((r, c))
                    board[r][c] = 'F'
                    moves += 1
                    move_made = True
            
            # Reveal safe cells
            for r, c in safe_cells_found:
                if (r, c) not in revealed:
                    revealed.add((r, c))
                    board[r][c] = internal_board[r][c]
                    moves += 1
                    move_made = True
            
            # If no certain moves, make probability-based guess
            if not move_made and probabilities:
                best_cell = min(probabilities.items(), key=lambda x: x[1])
                r, c = best_cell[0]
                if (r, c) not in revealed and (r, c) not in flags:
                    if (r, c) in mine_positions:
                        # Hit a mine - game over
                        break
                    else:
                        revealed.add((r, c))
                        board[r][c] = internal_board[r][c]
                        moves += 1
                        move_made = True
            
            if not move_made:
                break
        
        # Check win condition
        game_won = len(revealed) == rows * cols - mines
        solve_time = time.time() - start_time
        
        # Collect training data
        training_data = {
            "board_size": (rows, cols),
            "mine_count": mines,
            "moves": moves,
            "solve_time": solve_time,
            "game_won": game_won,
            "cells_revealed": len(revealed),
            "cells_flagged": len(flags),
            "accuracy": len(revealed) / (rows * cols - mines) if mines > 0 else 0,
            "efficiency": len(revealed) / moves if moves > 0 else 0
        }
        
        return training_data
    
    def train_batch(self, num_games: int = 100) -> Dict[str, float]:
        """Train AI on a batch of games."""
        print(f"🧠 Training batch: {num_games} games (parallel)")

        batch_results = []
        start_time = time.time()

        # Prepare tasks
        tasks = []
        for i in range(num_games):
            rows = random.choice([8, 10, 12, 16])
            cols = random.choice([8, 10, 12, 16])
            mines = int(rows * cols * random.uniform(0.1, 0.25))
            tasks.append((rows, cols, mines))

        max_workers = min(8, (os.cpu_count() or 4))
        with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as ex:
            futures = [ex.submit(self.simulate_game, r, c, m) for (r, c, m) in tasks]
            for i, fut in enumerate(concurrent.futures.as_completed(futures), start=1):
                try:
                    result = fut.result()
                except Exception as e:
                    print(f"❌ Simulation error: {e}")
                    continue

                batch_results.append(result)

                # Update current session
                if self.current_session:
                    self.current_session.games_played += 1
                    if result.get('game_won'):
                        self.current_session.games_won += 1
                    self.current_session.learning_data.append(result)

                # Progress indicator every 10 completed
                if i % 10 == 0 or i == num_games:
                    print(f"  📊 Progress: {i}/{num_games} games")

        # Calculate batch metrics
        batch_time = time.time() - start_time
        wins = sum(1 for r in batch_results if r.get('game_won'))
        win_rate = wins / len(batch_results) if batch_results else 0.0
        avg_time = statistics.mean([r['solve_time'] for r in batch_results]) if batch_results else 0.0
        avg_accuracy = statistics.mean([r['accuracy'] for r in batch_results]) if batch_results else 0.0
        avg_efficiency = statistics.mean([r['efficiency'] for r in batch_results]) if batch_results else 0.0

        batch_metrics = {
            "games": len(batch_results),
            "win_rate": win_rate,
            "avg_time": avg_time,
            "accuracy": avg_accuracy,
            "efficiency": avg_efficiency,
            "training_time": batch_time
        }

        print(f"✅ Batch complete: {win_rate:.1%} win rate, {avg_time:.2f}s avg time")
        return batch_metrics
    
    def update_model_weights(self, batch_metrics: Dict[str, float]):
        """Update AI model weights based on training results."""
        # Learning algorithm - adjust weights based on performance
        performance = batch_metrics['win_rate']
        
        # Adjust probability weights
        if performance > 0.8:  # Good performance - reinforce current strategy
            self.ai_model.probability_weights["pattern_bonus"] *= 1.01
            self.ai_model.probability_weights["certainty_threshold"] *= 1.005
        elif performance < 0.5:  # Poor performance - adjust strategy
            self.ai_model.probability_weights["adjacent_mines"] *= 0.99
            self.ai_model.probability_weights["corner_penalty"] *= 0.98
            self.ai_model.strategy_parameters["risk_tolerance"] *= 1.02
        
        # Update strategy parameters
        if batch_metrics['efficiency'] > 0.8:
            self.ai_model.strategy_parameters["pattern_recognition"] *= 1.01
        elif batch_metrics['efficiency'] < 0.5:
            self.ai_model.strategy_parameters["exploration_rate"] *= 1.02
        
        # Ensure weights stay in reasonable bounds
        for key in self.ai_model.probability_weights:
            self.ai_model.probability_weights[key] = max(0.1, min(2.0, self.ai_model.probability_weights[key]))
        
        for key in self.ai_model.strategy_parameters:
            self.ai_model.strategy_parameters[key] = max(0.0, min(1.0, self.ai_model.strategy_parameters[key]))
    
    def learn_patterns(self, training_data: List[Dict[str, Any]]):
        """Learn patterns from training data."""
        # Analyze successful games for patterns
        successful_games = [data for data in training_data if data['game_won']]
        
        if len(successful_games) < 5:
            return
        
        # Extract patterns
        board_sizes = [(data['board_size'][0], data['board_size'][1]) for data in successful_games]
        mine_ratios = [data['mine_count'] / (data['board_size'][0] * data['board_size'][1]) for data in successful_games]
        
        # Update learned patterns
        self.ai_model.learned_patterns.update({
            "optimal_board_sizes": board_sizes[:5],  # Top 5 board sizes
            "optimal_mine_ratios": mine_ratios[:5],  # Top 5 mine ratios
            "avg_moves_per_win": statistics.mean([data['moves'] for data in successful_games]),
            "avg_time_per_win": statistics.mean([data['solve_time'] for data in successful_games])
        })
    
    def finish_training_session(self):
        """Finish current training session and update model."""
        if not self.current_session:
            return
        
        # Calculate session metrics
        session = self.current_session
        session.win_rate = session.games_won / session.games_played if session.games_played > 0 else 0
        
        if session.learning_data:
            session.avg_solve_time = statistics.mean([data['solve_time'] for data in session.learning_data])
            session.best_solve_time = min([data['solve_time'] for data in session.learning_data])
            
            # Accuracy metrics
            session.accuracy_metrics = {
                "avg_accuracy": statistics.mean([data['accuracy'] for data in session.learning_data]),
                "avg_efficiency": statistics.mean([data['efficiency'] for data in session.learning_data]),
                "total_moves": sum([data['moves'] for data in session.learning_data])
            }
        
        # Update model
        previous_total_games = self.ai_model.total_games
        previous_total_wins = int(round(self.ai_model.overall_win_rate * previous_total_games))

        self.ai_model.training_sessions += 1
        self.ai_model.total_games += session.games_played

        # Update overall win rate safely
        new_total_games = self.ai_model.total_games
        new_total_wins = previous_total_wins + session.games_won
        self.ai_model.overall_win_rate = (new_total_wins / new_total_games) if new_total_games > 0 else 0.0
        
        # Add to performance history
        self.ai_model.performance_history.append({
            "session_id": session.session_id,
            "timestamp": session.timestamp,
            "win_rate": session.win_rate,
            "avg_time": session.avg_solve_time,
            "games": session.games_played
        })
        
        # Keep only last 50 sessions in history
        if len(self.ai_model.performance_history) > 50:
            self.ai_model.performance_history = self.ai_model.performance_history[-50:]
        
        # Add to training history
        self.training_history.append(session)
        
        # Save everything
        self.save_model()
        self.save_training_history()
        
        print(f"🎉 Training session completed: {session.session_id}")
        print(f"📊 Session results: {session.win_rate:.1%} win rate, {session.avg_solve_time:.2f}s avg time")
        print(f"🧠 Model updated: {self.ai_model.model_id} v{self.ai_model.version}")
        
        self.current_session = None
    
    def train_comprehensive(self, total_games: int = 1000) -> Dict[str, Any]:
        """Comprehensive training with multiple sessions."""
        print(f"🚀 Starting comprehensive training: {total_games} games")
        
        start_time = time.time()
        total_batches = total_games // self.batch_size
        
        for batch_num in range(total_batches):
            print(f"\n📚 Batch {batch_num + 1}/{total_batches}")
            
            # Start new session
            self.start_training_session((10, 10), 15)
            
            # Train batch
            batch_metrics = self.train_batch(self.batch_size)
            
            # Update model
            self.update_model_weights(batch_metrics)
            
            # Learn patterns
            if self.current_session and self.current_session.learning_data:
                self.learn_patterns(self.current_session.learning_data)
            
            # Finish session
            self.finish_training_session()
            
            # Show progress
            overall_win_rate = self.ai_model.overall_win_rate
            print(f"🎯 Overall progress: {overall_win_rate:.1%} win rate")
        
        total_time = time.time() - start_time
        
        results = {
            "total_games": total_games,
            "total_time": total_time,
            "final_win_rate": self.ai_model.overall_win_rate,
            "training_sessions": self.ai_model.training_sessions,
            "model_version": self.ai_model.version
        }
        
        print(f"\n🎉 Comprehensive training completed!")
        print(f"📊 Final results: {results['final_win_rate']:.1%} win rate")
        print(f"⏱️ Total training time: {total_time:.1f}s")
        print(f"🧠 Model: {self.ai_model.model_id} v{self.ai_model.version}")
        
        return results
    
    def evaluate_model(self, test_games: int = 100) -> Dict[str, float]:
        """Evaluate current AI model performance."""
        print(f"🧪 Evaluating model: {test_games} test games")
        
        test_results = []
        
        for i in range(test_games):
            rows = random.choice([8, 10, 12, 16])
            cols = random.choice([8, 10, 12, 16])
            mines = int(rows * cols * random.uniform(0.1, 0.25))
            
            result = self.simulate_game(rows, cols, mines)
            test_results.append(result)
        
        # Calculate metrics
        wins = sum(1 for r in test_results if r['game_won'])
        win_rate = wins / len(test_results)
        avg_time = statistics.mean([r['solve_time'] for r in test_results])
        avg_accuracy = statistics.mean([r['accuracy'] for r in test_results])
        avg_efficiency = statistics.mean([r['efficiency'] for r in test_results])
        
        metrics = {
            "win_rate": win_rate,
            "avg_time": avg_time,
            "accuracy": avg_accuracy,
            "efficiency": avg_efficiency,
            "test_games": len(test_results)
        }
        
        print(f"📊 Evaluation results:")
        print(f"  🎯 Win rate: {win_rate:.1%}")
        print(f"  ⏱️ Avg time: {avg_time:.2f}s")
        print(f"  🎯 Accuracy: {avg_accuracy:.1%}")
        print(f"  ⚡ Efficiency: {avg_efficiency:.1%}")
        
        return metrics
    
    def show_training_stats(self):
        """Display comprehensive training statistics."""
        print("\n" + "="*60)
        print("🤖 CYBERPUNK AI TRAINING STATISTICS")
        print("="*60)
        
        print(f"\n📊 Model Information:")
        print(f"  🆔 Model ID: {self.ai_model.model_id}")
        print(f"  📦 Version: {self.ai_model.version}")
        print(f"  🎓 Training Sessions: {self.ai_model.training_sessions}")
        print(f"  🎮 Total Games: {self.ai_model.total_games}")
        print(f"  🏆 Overall Win Rate: {self.ai_model.overall_win_rate:.1%}")
        
        print(f"\n⚙️ Model Parameters:")
        print(f"  🎯 Probability Weights:")
        for key, value in self.ai_model.probability_weights.items():
            print(f"    {key}: {value:.3f}")
        
        print(f"  🧠 Strategy Parameters:")
        for key, value in self.ai_model.strategy_parameters.items():
            print(f"    {key}: {value:.3f}")
        
        print(f"\n📚 Learned Patterns:")
        for key, value in self.ai_model.learned_patterns.items():
            if isinstance(value, list):
                print(f"  {key}: {value[:3]}...")  # Show first 3 items
            else:
                print(f"  {key}: {value}")
        
        print(f"\n📈 Recent Performance:")
        recent_sessions = self.ai_model.performance_history[-5:]
        for session in recent_sessions:
            timestamp = time.strftime("%H:%M:%S", time.localtime(session['timestamp']))
            print(f"  {timestamp}: {session['win_rate']:.1%} win rate, {session['avg_time']:.2f}s")
        
        print("="*60)


def main():
    """Main training interface."""
    trainer = CyberpunkAITrainer()
    
    print("\n🤖 CYBERPUNK AI TRAINER")
    print("=" * 50)
    print("1. Quick Training (100 games)")
    print("2. Comprehensive Training (1000 games)")
    print("3. Evaluate Current Model")
    print("4. Show Training Statistics")
    print("5. Exit")
    
    while True:
        choice = input("\n🎯 Select option (1-5): ").strip()
        
        if choice == "1":
            print("\n🚀 Starting quick training...")
            trainer.start_training_session((10, 10), 15)
            batch_metrics = trainer.train_batch(100)
            trainer.update_model_weights(batch_metrics)
            trainer.learn_patterns(trainer.current_session.learning_data)
            trainer.finish_training_session()
            
        elif choice == "2":
            print("\n🚀 Starting comprehensive training...")
            trainer.train_comprehensive(1000)
            
        elif choice == "3":
            print("\n🧪 Evaluating current model...")
            trainer.evaluate_model(100)
            
        elif choice == "4":
            trainer.show_training_stats()
            
        elif choice == "5":
            print("👋 Exiting AI trainer...")
            break
            
        else:
            print("❌ Invalid choice. Please select 1-5.")


if __name__ == "__main__":
    main()
