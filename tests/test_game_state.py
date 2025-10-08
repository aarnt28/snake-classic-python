from __future__ import annotations

import random

import pytest

from snake_classic.core.difficulty import get_difficulty
from snake_classic.core.direction import Direction
from snake_classic.core.game_state import GameState


@pytest.fixture(autouse=True)
def deterministic_random(monkeypatch):
    rng = random.Random(0)

    def choice(seq):
        return rng.choice(list(seq))

    monkeypatch.setattr(random, "choice", choice)


def test_food_spawns_outside_snake_body():
    difficulty = get_difficulty("classic")
    state = GameState.create((10, 10), difficulty)
    assert not state.snake.occupies(state.food)


def test_scoring_and_growth_on_food_consumption():
    difficulty = get_difficulty("classic")
    state = GameState.create((10, 10), difficulty)
    state.food = (state.snake.head[0] + 1, state.snake.head[1])
    state.update_direction(Direction.RIGHT)
    state.step()
    assert state.score == difficulty.points
    assert len(list(state.snake.segments())) == 4


def test_game_over_on_wall_collision():
    difficulty = get_difficulty("relaxed")
    state = GameState.create((4, 4), difficulty)
    state.update_direction(Direction.LEFT)
    for _ in range(3):
        state.step()
    assert state.game_over


def test_game_reset_returns_to_initial_state():
    difficulty = get_difficulty("classic")
    state = GameState.create((10, 10), difficulty)
    state.score = 100
    state.game_over = True
    state.reset()
    assert state.score == 0
    assert not state.game_over
    assert not state.snake.occupies(state.food)


def test_grid_must_be_large_enough():
    difficulty = get_difficulty("classic")
    with pytest.raises(ValueError):
        GameState.create((3, 10), difficulty)
