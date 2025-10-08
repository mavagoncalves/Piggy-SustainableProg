# -------------------------------------
# Makefile for Pig (Dice Game) Project
# -------------------------------------

# Variables
PY = python3
PIP = pip
SRC = src/pig            # package folder (you can change to "." until you have src/)
TESTS = tests

# -------------- BASIC COMMANDS ----------------

# Create and activate a virtual environment
venv:
	$(PY) -m venv .venv
	.venv/bin/$(PIP) install -U pip

# Install dependencies from requirements.txt
install:
	.venv/bin/$(PIP) install -r requirements.txt

# Run the game
run:
	.venv/bin/$(PY) main.py

# -------------- TESTING & COVERAGE ----------------

# Run all tests quietly
test:
	PYTHONPATH=. .venv/bin/pytest -v

# Run tests with coverage
coverage:
	.venv/bin/pytest --cov=$(SRC) --cov-report=term-missing --cov-report=html

# -------------- CODE QUALITY ----------------

# Run linting (flake8 + pylint)
lint:
	.venv/bin/flake8 $(SRC) $(TESTS)
	- .venv/bin/pylint $(SRC) || true

# Auto-format code
format:
	.venv/bin/black $(SRC) $(TESTS)
	.venv/bin/isort $(SRC) $(TESTS)

# -------------- DOCUMENTATION ----------------

# Generate HTML documentation from docstrings
doc:
	mkdir -p doc/api
	.venv/bin/pdoc --html --output-dir doc/api --force $(SRC)

# Generate UML diagrams (class & package)
uml:
	mkdir -p doc/uml
	.venv/bin/pyreverse -o dot -p PigUML -A -S $(SRC)
	dot -Tsvg classes_PigUML.dot -o doc/uml/class.svg
	dot -Tsvg packages_PigUML.dot -o doc/uml/package.svg

# -------------- CLEANUP ----------------

# Clean all generated files
clean:
	rm -rf __pycache__ .pytest_cache htmlcov doc/api doc/uml *.dot .pyreverse .venv

