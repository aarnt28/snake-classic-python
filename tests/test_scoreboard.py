from __future__ import annotations

from pathlib import Path

from snake_classic.scoreboard import Scoreboard


def test_scoreboard_persists_entries(tmp_path: Path):
    board = Scoreboard(path=tmp_path / "scores.json", limit=3)
    board.submit("Alice", 100, "classic")
    board.submit("Bob", 50, "relaxed")
    board.submit("Carol", 200, "extreme")
    board.submit("Dan", 75, "classic")

    entries = board.load()
    assert [entry.name for entry in entries] == ["Carol", "Alice", "Dan"]
    assert entries[0].score == 200
