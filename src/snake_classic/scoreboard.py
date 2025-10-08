from __future__ import annotations

import json
import os
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Iterable, List


@dataclass
class ScoreEntry:
    name: str
    score: int
    difficulty: str
    achieved_at: str


class Scoreboard:
    """Minimal JSON based persistent storage for high scores."""

    def __init__(self, path: Path | None = None, limit: int = 25) -> None:
        self.limit = limit
        default_dir = Path(os.environ.get("SNAKE_CLASSIC_HOME", str(Path.home() / ".snake_classic")))
        self.path = path or (default_dir / "scores.json")
        self.path.parent.mkdir(parents=True, exist_ok=True)

    def load(self) -> List[ScoreEntry]:
        if not self.path.exists():
            return []
        try:
            data = json.loads(self.path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            # Corrupted file? start fresh but do not delete automatically.
            return []
        entries = [ScoreEntry(**entry) for entry in data]
        return sorted(entries, key=lambda e: e.score, reverse=True)[: self.limit]

    def save(self, entries: Iterable[ScoreEntry]) -> None:
        payload = [entry.__dict__ for entry in entries]
        self.path.write_text(json.dumps(payload, indent=2), encoding="utf-8")

    def submit(self, name: str, score: int, difficulty: str) -> List[ScoreEntry]:
        entries = self.load()
        now = datetime.now(UTC).isoformat(timespec="seconds")
        entries.append(ScoreEntry(name=name, score=score, difficulty=difficulty, achieved_at=now))
        entries = sorted(entries, key=lambda e: e.score, reverse=True)[: self.limit]
        self.save(entries)
        return entries
