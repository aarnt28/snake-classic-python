# Snake Classic – Python Edition

This project is a Python-first alternative to the original [SnakeClassic](https://github.com/aarnt28/SnakeClassic) repository.  Instead of a browser game backed by FastAPI, this version recreates the classic arcade gameplay using [Pygame](https://www.pygame.org/) and keeps a simple JSON leaderboard on disk.

## Features

- **Modern Python codebase** – structured as a package with reusable core logic and unit tests.
- **Multiple difficulties** – relaxed, classic, arcade, and extreme presets that change the game speed and scoring.
- **Keyboard friendly controls** – supports arrow keys or WASD.
- **Persistent leaderboard** – scores are stored in `~/.snake_classic/scores.json` by default.
- **Docker ready** – run the game in a container with an attached display server.

## Getting started

### Local environment

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python -m snake_classic --difficulty classic
```

When the game ends you can press **Enter** to play again or **Esc** to quit.  If you achieved a positive score you will be prompted in the terminal to record your name on the leaderboard.

### Running the tests

```bash
pip install -r requirements-dev.txt
pytest
```

### Docker

The repository includes a `Dockerfile` that installs the necessary dependencies.  When running via Docker you must expose your X11 or Wayland display to the container.  On Linux with X11 this can be done with:

```bash
docker build -t snake-classic-python .
docker run \
  --rm \
  -e DISPLAY \
  -v /tmp/.X11-unix:/tmp/.X11-unix \
  snake-classic-python
```

## Controls

| Action      | Key bindings       |
| ----------- | ------------------ |
| Move up     | Arrow Up / W       |
| Move down   | Arrow Down / S     |
| Move left   | Arrow Left / A     |
| Move right  | Arrow Right / D    |
| Quit game   | Esc / Q            |
| Restart     | Enter              |

## Leaderboard storage

Scores are stored in JSON format.  By default the file lives in `~/.snake_classic/scores.json`.  Set the `SNAKE_CLASSIC_HOME` environment variable to override the directory.

## License

This project is released under the MIT License.
