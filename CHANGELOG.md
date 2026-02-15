# Changelog

## Unreleased

- Performance: Cache neighbor lookups in `advanced_solver.py` to avoid repeated recomputation.
- Performance: `calculate_probabilities()` now uses exact enumeration for small constraint sets and Monte Carlo sampling for large sets to avoid exponential blowups.
- Trainer: `ai_trainer.py` `train_batch()` parallelized using `ThreadPoolExecutor` and progress reporting improved.
- Trainer: Fixed overall win-rate calculation bug.
- UI: Debounced logic feed updates and replaced blocking `time.sleep()` in auto-solver with scheduled `root.after` actions for non-blocking responsiveness.
- Added `requirements.txt` listing `numpy`, `pygame`, and optional `numba`.
- Created automated quick-evaluation benchmark (used `CyberpunkAITrainer.evaluate_model(20)` during validation).

