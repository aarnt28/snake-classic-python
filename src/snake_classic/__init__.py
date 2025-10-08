"""Snake Classic - Python Edition.

This package provides a Pygame powered recreation of the classic Snake game
with a JSON backed leaderboard.  The gameplay mechanics are intentionally
minimal so that the core logic can be easily tested and extended.
"""

from .game import GameConfig, SnakeGame, main

__all__ = ["GameConfig", "SnakeGame", "main"]
