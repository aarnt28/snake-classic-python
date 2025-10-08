from __future__ import annotations

import pytest

from snake_classic.core.direction import Direction
from snake_classic.core.snake import Snake


def test_snake_creation_requires_minimum_segments():
    with pytest.raises(ValueError):
        Snake.create([(0, 0)], Direction.RIGHT)


def test_snake_moves_forward_and_grows():
    snake = Snake.create([(2, 0), (1, 0), (0, 0)], Direction.RIGHT)
    snake.grow()
    new_head = snake.step()
    assert new_head == (3, 0)
    assert list(snake.segments()) == [(3, 0), (2, 0), (1, 0), (0, 0)]


def test_snake_ignores_reverse_direction():
    snake = Snake.create([(2, 0), (1, 0), (0, 0)], Direction.RIGHT)
    snake.step(Direction.LEFT)
    assert snake.head == (3, 0)
    assert snake.direction == Direction.RIGHT


def test_self_collision_detection():
    snake = Snake.create([(2, 2), (2, 3), (1, 3), (1, 2)], Direction.UP)
    snake.grow(1)
    snake.step(Direction.LEFT)
    assert snake.self_collision()
