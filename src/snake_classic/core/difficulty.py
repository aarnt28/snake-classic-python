from __future__ import annotations

from dataclasses import dataclass
from typing import Dict


@dataclass(frozen=True)
class Difficulty:
    name: str
    speed: int  # Frames per second
    growth: int  # Segments gained per food
    points: int  # Points per food


DEFAULT_DIFFICULTIES: Dict[str, Difficulty] = {
    "relaxed": Difficulty(name="relaxed", speed=8, growth=1, points=5),
    "classic": Difficulty(name="classic", speed=12, growth=1, points=10),
    "arcade": Difficulty(name="arcade", speed=18, growth=2, points=15),
    "extreme": Difficulty(name="extreme", speed=22, growth=3, points=25),
}


def get_difficulty(name: str | None) -> Difficulty:
    if not name:
        return DEFAULT_DIFFICULTIES["classic"]
    name = name.lower()
    return DEFAULT_DIFFICULTIES.get(name, DEFAULT_DIFFICULTIES["classic"])
