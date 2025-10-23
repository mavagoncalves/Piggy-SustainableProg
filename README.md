# Piggy Dice Game

| ![Python](https://img.shields.io/badge/Python3.10-yellow?style=flat&logo=python) | ![Pytest](https://img.shields.io/badge/Pytest-green?style=flat&logo=pytest) | ![Static Badge](https://img.shields.io/badge/Makefile-pink?style=flat&logo=Make) | ![Static Badge](https://img.shields.io/badge/Pylint%20-%20blue?logo=pylint)  |
|---|---|---|---|

A command-line implementation of the Pig Dice Game, playable between two human players or against an AI opponent with multiple difficulty levels.  
The project uses a `Makefile` for setup and tasks, a `menu.py` entry point for the main menu flow, and persists highscores between runs.

---

## Features

- Two-player and vs AI modes
- AI with easy, medium, and hard difficulties
- Dice system with configurable sides
- Cheat menu to add or subtract points manually (for testing or fun)
- Winner detection at 100 points
- Persistent highscore storage
- Makefile-driven setup, run, and test commands
- Unit tests with pytest

---

## Project Structure

```
Piggy/
│
├── src/
│   ├── menu.py          # Application entry point (main menu / CLI)
│   ├── highscore.py     # Highscore save
│   ├── game.py          # Main game logic
│   ├── player.py        # Player class
│   ├── dice.py          # Dice behavior
│   ├── ai.py            # AI decision logic
│   ├── cheat.py         # Hidden game cheats
│   └── cli.py           # CLI
│
├── data/
│   └── highscore.json   # Highscore persistence file (created on first save)
│
├── doc/
│   ├── api/             # HTML documentatiom
│   └── uml/             # UML class diagram
│
├── tools/
│   └── uml_build.py     # UML build helper
│
├── tests/
│   ├── test_game.py
│   ├── test_ai.py
│   ├── test_dice.py
│   ├── test_player.py
│   ├── test_highscore.py
│   ├── test_cheat.py
│   ├── test_cli.py
│   └── test_menu.py
│
├── main.py
├── Makefile
├── requirements.txt
└── README.md
```

---

## Requirements

- Python 3.10 or higher  
- `make` utility installed (default on macOS/Linux, available via Git Bash on Windows)

---

## Setup

All setup steps can be run using the provided Makefile.

### 1. Create a virtual environment and install dependencies:
```bash
make venv
```

This will:
- Create a `.venv` virtual environment
- Install dependencies listed in `requirements.txt`
- Install `pytest` if not already included

### 2. Activate the environment (if needed):
```bash
source .venv/bin/activate     # macOS/Linux
.venv\Scripts\activate        # Windows
```

---

## Running the Game

Run the game using:
```bash
make run
```

This is equivalent to:
```bash
python -m src.game
```

---

## How to Play

1. Choose whether to play against another player or the AI.  
2. On your turn:
   - Press **r** to roll the dice.  
   - Press **h** to hold and add your round score to your total.  
   - If you roll a 1, you lose your round score and your turn ends.  
3. The first player to reach 100 points wins.  
4. You can access the hidden cheat menu by typing `hidden` during your turn.

---

## AI Difficulty Levels

| Level | Description |
|--------|--------------|
| Easy | Takes more risks and holds less often |
| Medium | Balanced rolling and holding decisions |
| Hard | Plays strategically and holds wisely |

---

## Running Tests

Run all tests with:
```bash
make test
```
This executes:
```bash
pytest -v
```

All tests are located in the `tests/` directory.

---
## Building Documentation

We generate two kinds of docs:

1) **UML diagrams**
   - Built from source with `pyreverse` (via pylint), outputting `classes_<Project>.puml`
   - Rendered to PNG using **Kroki** (online). If offline, the build still produces the `.puml` and will warn about PNG rendering.

2) **API reference**
   - HTML generated with **pdoc** from everything inside `src/`

### Prerequisites
- Internet access for PNG rendering via Kroki (optional)

### One-time setup
```bash
make venv
make docs-dep
make docs
```
---
## Quality and coverage
- Quality checked with Pylint
- Coverage checked with Pytest

### Prerequisites
- Make sure you go through the *Setup* steps for the program

### Running coverage and lint

```bash
make quality
```

---

## Makefile Commands

| Command | Description |
|----------|-------------|
| `make venv` | Create and set up virtual environment |
| `make install` | Installs dependencies in `requirements.txt`|
| `make run` | Run the Pig Dice Game |
| `make test` | Run all unit tests |
| `make quality` | Runs tests with lint and coverage checking |
| `make clean` | Remove virtual environment and cache files |
| `make docs-dep` | Install python dependencies for documentation |
| `make docs` | Build both API docs and UML PNGs |


---

## Development Notes

- Requires Python 3.10 or higher
- TDD -> Programmed using test driven development 
- Command-line interface only  
- Modular code structure for easy maintenance and extension  
- Tested with pytest  

---



## Authors

- [@mavagoncalves](https://www.github.com/mavagoncalves)
- [@ayahassaad](https://www.github.com/ayahassaad)
- [@robrodres](https://www.github.com/robrodres)




