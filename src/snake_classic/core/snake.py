from __future__ import annotations

from collections import deque
from dataclasses import dataclass, field
from typing import Deque, Iterable, Iterator, Tuple

from .direction import Direction

Coordinate = Tuple[int, int]


@dataclass
class Snake:
    """Represents the snake body and handles movement and growth."""

    body: Deque[Coordinate] = field(default_factory=deque)
    direction: Direction = Direction.RIGHT
    grow_segments: int = 0

    @staticmethod
    def create(initial: Iterable[Coordinate], direction: Direction) -> "Snake":
        body = deque(initial)
        if len(body) < 2:
            raise ValueError("Snake must have at least two segments")
        return Snake(body=body, direction=direction)

    @property
    def head(self) -> Coordinate:
        return self.body[0]

    def occupies(self, point: Coordinate) -> bool:
        return point in self.body

    def next_head(self, direction: Direction | None = None) -> Coordinate:
        direction = direction or self.direction
        dx, dy = direction.vector
        hx, hy = self.head
        return hx + dx, hy + dy

    def step(self, direction: Direction | None = None) -> Coordinate:
        """Advance the snake and return the new head position."""

        if direction and direction != self.direction.opposite():
            self.direction = direction

        new_head = self.next_head()
        self.body.appendleft(new_head)

        if self.grow_segments > 0:
            self.grow_segments -= 1
        else:
            self.body.pop()

        return new_head

    def grow(self, amount: int = 1) -> None:
        self.grow_segments += amount

    def segments(self) -> Iterator[Coordinate]:
        return iter(self.body)

    def self_collision(self, point: Coordinate | None = None) -> bool:
        check_point = point or self.head
        body = list(self.body)
        # Skip the head position when checking collisions with the rest of the body.
        return check_point in body[1:]

    def reset(self, initial: Iterable[Coordinate], direction: Direction) -> None:
        self.body = deque(initial)
        self.direction = direction
        self.grow_segments = 0
