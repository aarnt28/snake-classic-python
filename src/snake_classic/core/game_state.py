from __future__ import annotations
import random
from dataclasses import dataclass
from typing import Iterable, List, Tuple

from .difficulty import Difficulty
from .direction import Direction, InputDirection
from .snake import Coordinate, Snake


GridSize = Tuple[int, int]


@dataclass
class GameState:
    grid_size: GridSize
    difficulty: Difficulty
    snake: Snake
    input_direction: InputDirection
    food: Coordinate
    score: int = 0
    game_over: bool = False

    @classmethod
    def create(cls, grid_size: GridSize, difficulty: Difficulty) -> "GameState":
        width, height = grid_size
        if width < 4 or height < 4:
            raise ValueError("Grid size must be at least 4x4")
        center = (width // 2, height // 2)
        snake = Snake.create(
            initial=[center, (center[0] - 1, center[1]), (center[0] - 2, center[1])],
            direction=Direction.RIGHT,
        )
        food = cls._random_food(grid_size, snake.body)
        return cls(
            grid_size=grid_size,
            difficulty=difficulty,
            snake=snake,
            input_direction=InputDirection(snake.direction),
            food=food,
        )

    @staticmethod
    def _random_food(grid_size: GridSize, occupied: Iterable[Coordinate]) -> Coordinate:
        width, height = grid_size
        occupied_set = set(occupied)
        possible: List[Coordinate] = [
            (x, y) for x in range(width) for y in range(height) if (x, y) not in occupied_set
        ]
        if not possible:
            raise RuntimeError("No space left for food")
        return random.choice(possible)

    def update_direction(self, requested: Direction) -> None:
        self.input_direction = self.input_direction.next(requested)

    def step(self) -> None:
        if self.game_over:
            return

        direction = self.input_direction.current
        new_head = self.snake.next_head(direction)
        width, height = self.grid_size
        hx, hy = new_head
        if hx < 0 or hy < 0 or hx >= width or hy >= height:
            self.game_over = True
            return
        will_grow = new_head == self.food
        if self._collides_with_body(new_head, will_grow):
            self.game_over = True
            return

        if will_grow:
            self.snake.grow(self.difficulty.growth)

        self.snake.step(direction)

        if will_grow:
            self.score += self.difficulty.points
            self.food = self._random_food(self.grid_size, self.snake.body)

        # Synchronize input direction with the snake's actual heading so that
        # repeated steps continue moving forward even if the player has not
        # provided additional input.
        self.input_direction = InputDirection(self.snake.direction)

    def _collides_with_body(self, new_head: Coordinate, will_grow: bool) -> bool:
        body = list(self.snake.body)
        # When the snake is not growing the tail will move forward, so standing
        # on the previous tail position is safe.
        if not will_grow:
            body = body[:-1]
        return new_head in body

    def reset(self) -> None:
        fresh = type(self).create(self.grid_size, self.difficulty)
        self.snake = fresh.snake
        self.input_direction = fresh.input_direction
        self.food = fresh.food
        self.score = 0
        self.game_over = False
