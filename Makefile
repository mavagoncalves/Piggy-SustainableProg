# -------------------------------------
# Makefile for Piggy (Dice Game) Project
# Cross-platform (macOS/Linux/Windows)
# -------------------------------------

SRC ?= src
TESTS ?= tests
VENV ?= .venv
COV_MIN ?= 80

ifeq ($(OS),Windows_NT)
SYS_PY := python
PY := $(VENV)/Scripts/python.exe
PIP := $(VENV)/Scripts/pip.exe
PATH_SEP := \\
else
SYS_PY := python3
PY := $(VENV)/bin/python
PIP := $(VENV)/bin/pip
PATH_SEP := /
endif

.PHONY: venv install run test clean doc-deps doc uml docs serve-doc clean-doc quality clean-quality

venv:
	$(SYS_PY) -m venv $(VENV)
	"$(PIP)" install -U pip

install: venv
	"$(PIP)" install -r requirements.txt

run: venv
	"$(PY)" main.py

test: venv
	"$(PY)" -m pytest -v

# Portable clean using Python (no rm/find flags)
clean:
	"$(PY)" -c "import shutil, pathlib; \
for p in map(pathlib.Path, ['__pycache__','.pytest_cache','htmlcov']): \
    shutil.rmtree(p, ignore_errors=True); \
print('✓ Cleaned build/test artifacts')"

# -------------------------------------
#             Documentation 
# -------------------------------------

DOC_DIR   ?= doc
API_DIR   ?= $(DOC_DIR)/api
UML_DIR   ?= $(DOC_DIR)/uml
PROJECT   ?= Piggy
SRC_ABS   := $(abspath $(SRC))

# Python modules via the venv
PDOC_MOD      := pdoc
PY2PUML_MOD   := py2puml
PYDEPS_CMD    := pydeps

# Install Python-only deps (works on macOS & Windows)
doc-deps: venv
	"$(PIP)" install -U pdoc py2puml pydeps requests
	@echo "✓ Installed: pdoc, py2puml, pydeps, requests"

# Generate HTML API docs -> doc/api (portable mkdir)
doc: venv
	"$(PY)" -c "import os; os.makedirs(r'$(API_DIR)', exist_ok=True)"
	"$(PY)" -c "import sys, runpy, importlib.util; sys.path.insert(0, r'$(SRC)'); \
sys.argv=['pdoc','-o', r'$(API_DIR)','--docformat','google','--no-show-source', r'$(SRC)']; \
m='pdoc.__main__'; runpy.run_module(m if importlib.util.find_spec(m) else 'pdoc', run_name='__main__'); \
print('✓ API documentation: $(API_DIR)/index.html')"

# Generate UML diagrams as PNGs into doc/uml (no Graphviz)
uml: venv
	"$(PY)" -c "import os; os.makedirs(r'$(UML_DIR)', exist_ok=True)"
	"$(PY)" tools/uml_build.py --project "$(PROJECT)" --src "$(SRC)" --out "$(UML_DIR)"

# Build both API docs and UML PNGs
docs: doc uml
	@echo "✓ Full documentation written to: $(DOC_DIR)/"

# Serve API docs locally (http://127.0.0.1:8080)
serve-doc: venv
	"$(PY)" -m $(PDOC_MOD) --http :8080 "$(SRC)"

# Clean only generated documentation (portable)
clean-doc:
	"$(PY)" -c "import shutil, pathlib; \
[shutil.rmtree(pathlib.Path(p), ignore_errors=True) for p in [r'$(API_DIR)', r'$(UML_DIR)']]; \
print('✓ Documentation cleaned.')"

# -------------------------------------
#        Coverage and quality
# -------------------------------------

quality: venv
	"$(PIP)" install -U pip
	"$(PIP)" install pytest pytest-cov pylint
	@echo "Running pylint..."
	"$(PY)" -m pylint "$(SRC)" || true
	@echo "Running tests with coverage (min $(COV_MIN)%)..."
	"$(PY)" -m pytest "$(TESTS)" \
		--maxfail=1 \
		--cov="$(SRC)" \
		--cov-fail-under=$(COV_MIN) \
		--cov-report=term-missing
	@echo "✓ Quality check passed"

clean-quality:
	"$(PY)" -c "import shutil, pathlib, os; \
shutil.rmtree('.coverage', ignore_errors=True); \
shutil.rmtree('htmlcov', ignore_errors=True); \
shutil.rmtree('.pytest_cache', ignore_errors=True); \
from pathlib import Path; \
[shutil.rmtree(p, ignore_errors=True) for p in Path('$(SRC)').rglob('__pycache__') if p.is_dir()]; \
print('✓ Cleaned quality artifacts')"
