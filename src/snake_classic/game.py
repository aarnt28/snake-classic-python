from __future__ import annotations

import argparse
from dataclasses import dataclass
from typing import Iterable

import pygame

from .core.difficulty import DEFAULT_DIFFICULTIES, Difficulty, get_difficulty
from .core.direction import Direction
from .core.game_state import GameState
from .renderer import GameRenderer
from .scoreboard import Scoreboard


@dataclass
class GameConfig:
    grid_width: int = 24
    grid_height: int = 18
    cell_size: int = 28
    difficulty: str = "classic"
    score_limit: int = 25


class SnakeGame:
    def __init__(self, config: GameConfig | None = None) -> None:
        self.config = config or GameConfig()
        self.difficulty: Difficulty = get_difficulty(self.config.difficulty)
        self.state = GameState.create(
            grid_size=(self.config.grid_width, self.config.grid_height),
            difficulty=self.difficulty,
        )
        self.renderer = GameRenderer(cell_size=self.config.cell_size)
        self.scoreboard = Scoreboard(limit=self.config.score_limit)

    def run(self) -> None:
        pygame.init()
        window = pygame.display.set_mode(
            (
                self.config.grid_width * self.config.cell_size,
                self.config.grid_height * self.config.cell_size,
            )
        )
        pygame.display.set_caption("Snake Classic - Python Edition")
        clock = pygame.time.Clock()

        running = True
        while running:
            requested_direction = None
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key in (pygame.K_q, pygame.K_ESCAPE):
                        running = False
                    elif event.key in (pygame.K_RETURN, pygame.K_KP_ENTER) and self.state.game_over:
                        self._handle_game_over(confirm=True)
                    elif not self.state.game_over:
                        requested_direction = self._direction_from_key(event.key)

            if requested_direction:
                self.state.update_direction(requested_direction)

            if not self.state.game_over:
                self.state.step()
            else:
                self._handle_game_over(confirm=False)

            self.renderer.draw(window, self.state)
            pygame.display.flip()
            clock.tick(self.difficulty.speed)

        pygame.quit()

    def _direction_from_key(self, key: int) -> Direction | None:
        mapping = {
            pygame.K_UP: Direction.UP,
            pygame.K_w: Direction.UP,
            pygame.K_DOWN: Direction.DOWN,
            pygame.K_s: Direction.DOWN,
            pygame.K_LEFT: Direction.LEFT,
            pygame.K_a: Direction.LEFT,
            pygame.K_RIGHT: Direction.RIGHT,
            pygame.K_d: Direction.RIGHT,
        }
        return mapping.get(key)

    def _handle_game_over(self, confirm: bool) -> None:
        if confirm:
            self._maybe_record_score()
            self.state.reset()
        else:
            # Passive prompt to encourage recording high score.
            pass

    def _maybe_record_score(self) -> None:
        if self.state.score <= 0:
            return
        name = self._prompt_name()
        entries = self.scoreboard.submit(name=name, score=self.state.score, difficulty=self.difficulty.name)
        self._print_leaderboard(entries)

    def _prompt_name(self) -> str:
        # PyGame doesn't include UI widgets. We prompt in the console.
        try:
            return input("Great job! Enter your name for the leaderboard (leave blank for Anonymous): ") or "Anonymous"
        except EOFError:
            return "Anonymous"

    def _print_leaderboard(self, entries) -> None:
        print("\n=== Leaderboard ===")
        for index, entry in enumerate(entries, start=1):
            print(f"{index:>2}. {entry.name:<16} {entry.score:>5} pts [{entry.difficulty}] on {entry.achieved_at}")
        print("===================\n")


def _grid_size(value: str) -> int:
    integer = int(value)
    if integer < 4:
        raise argparse.ArgumentTypeError("Grid dimensions must be at least 4")
    return integer


def parse_args(args: Iterable[str] | None = None) -> GameConfig:
    parser = argparse.ArgumentParser(description="Play a modern Python recreation of Snake Classic")
    parser.add_argument("--width", type=_grid_size, default=24, help="Number of grid cells horizontally")
    parser.add_argument("--height", type=_grid_size, default=18, help="Number of grid cells vertically")
    parser.add_argument("--cell-size", type=int, default=28, help="Pixel size of each grid cell")
    parser.add_argument(
        "--difficulty",
        choices=sorted(DEFAULT_DIFFICULTIES.keys()),
        default="classic",
        help="Predefined difficulty preset",
    )
    parser.add_argument(
        "--scores",
        type=int,
        default=25,
        help="Maximum number of leaderboard entries to retain",
    )
    namespace = parser.parse_args(args=args)
    return GameConfig(
        grid_width=namespace.width,
        grid_height=namespace.height,
        cell_size=namespace.cell_size,
        difficulty=namespace.difficulty,
        score_limit=namespace.scores,
    )


def main(argv: Iterable[str] | None = None) -> None:
    config = parse_args(argv)
    game = SnakeGame(config)
    game.run()


if __name__ == "__main__":
    main()
