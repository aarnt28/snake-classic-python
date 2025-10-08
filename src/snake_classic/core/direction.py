from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class Direction(Enum):
    """Possible movement directions for the snake."""

    UP = (0, -1)
    DOWN = (0, 1)
    LEFT = (-1, 0)
    RIGHT = (1, 0)

    @property
    def vector(self) -> tuple[int, int]:
        return self.value

    def opposite(self) -> "Direction":
        dx, dy = self.vector
        return Direction((-dx, -dy))

    @staticmethod
    def from_vector(vector: tuple[int, int]) -> "Direction":
        for direction in Direction:
            if direction.vector == vector:
                return direction
        raise ValueError(f"Unknown direction vector: {vector}")


@dataclass(frozen=True)
class InputDirection:
    """Represents an input direction request from the player.

    The snake cannot reverse direction immediately.  This helper keeps
    the desired direction and ensures it only changes to legal values.
    """

    current: Direction

    def next(self, requested: Direction) -> "InputDirection":
        if requested == self.current.opposite():
            # Ignore 180-degree turns.
            return self
        return InputDirection(requested)
