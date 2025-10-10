# -------------------------------------
# Makefile for Pig (Dice Game) Project
# Cross-platform (macOS/Linux/Windows)
# -------------------------------------

# -------------- VARIABLES ----------------
# Paths
SRC    ?= src           # you have ai.py, dice.py, player.py directly under src/
TESTS  ?= tests
VENV   ?= .venv

# Tools (OS-aware venv paths)
ifeq ($(OS),Windows_NT)
SYS_PY := python
PY     := $(VENV)/Scripts/python.exe
PIP    := $(VENV)/Scripts/pip.exe
else
SYS_PY := python3
PY     := $(VENV)/bin/python
PIP    := $(VENV)/bin/pip
endif

.PHONY: venv install run test coverage lint format doc uml clean distclean

# -------------- BASIC COMMANDS ----------------

# Create and upgrade virtual environment
venv:
	$(SYS_PY) -m venv $(VENV)
	"$(PIP)" install -U pip

# Install dependencies from requirements.txt
install: venv
	"$(PIP)" install -r requirements.txt

# Run the game
run: venv
	"$(PY)" main.py

# -------------- TESTING & COVERAGE ----------------

# Run all tests (pytest reads pythonpath from pytest.ini)
test: venv
	"$(PY)" -m pytest -v

# Run tests with coverage
coverage: venv
	"$(PY)" -m pytest --cov=$(SRC) --cov-report=term-missing --cov-report=html

# -------------- CODE QUALITY ----------------

# Run linting (flake8 + pylint)
lint: venv
	"$(PY)" -m flake8 $(SRC) $(TESTS)
	- "$(PY)" -m pylint $(SRC)

# Auto-format code
format: venv
	"$(PY)" -m black $(SRC) $(TESTS)
	"$(PY)" -m isort $(SRC) $(TESTS)

# -------------- DOCUMENTATION ----------------

# Generate HTML documentation from docstrings
doc: venv
	"$(PY)" -m pdoc --html --output-dir doc/api --force $(SRC)

# Generate UML diagrams (class & package)
uml: venv
	"$(PY)" -m pylint.pyreverse -o dot -p PigUML -A -S $(SRC)
	mkdir -p doc/uml
	dot -Tsvg classes_PigUML.dot   -o doc/uml/class.svg
	dot -Tsvg packages_PigUML.dot  -o doc/uml/package.svg

# -------------- CLEANUP ----------------

# Clean all generated files (keeps the venv)
clean: venv
	"$(PY)" - <<'PY'
import shutil, glob, os
for p in ['__pycache__', '.pytest_cache', 'htmlcov', 'doc/api', 'doc/uml', '.pyreverse']:
    shutil.rmtree(p, ignore_errors=True)
for f in glob.glob('*.dot'):
    try: os.remove(f)
    except OSError: pass
PY

# Remove EVERYTHING including the virtualenv
distclean: clean
	$(SYS_PY) - <<'PY'
import shutil; shutil.rmtree('.venv', ignore_errors=True)
PY
