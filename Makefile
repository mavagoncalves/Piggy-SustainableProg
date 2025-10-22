# -------------------------------------
# Makefile for Pig (Dice Game) Project
# Cross-platform (macOS/Linux/Windows)
# -------------------------------------

SRC ?= src
TESTS ?= tests
VENV ?= .venv

ifeq ($(OS),Windows_NT)
SYS_PY := python
PY := $(VENV)/Scripts/python.exe
PIP := $(VENV)/Scripts/pip.exe
else
SYS_PY := python3
PY := $(VENV)/bin/python
PIP := $(VENV)/bin/pip
endif

.PHONY: venv install run test clean

venv:
	$(SYS_PY) -m venv $(VENV)
	"$(PIP)" install -U pip

install: venv
	"$(PIP)" install -r requirements.txt

run: venv
	"$(PY)" main.py

test: venv
	"$(PY)" -m pytest -v

clean:
	@rm -rf __pycache__ .pytest_cache htmlcov || true



# -------------------------------------
# Documentation (cross-platform, no Graphviz/pyreverse)
# - API docs: pdoc -> doc/api
# - UML class diagram: py2puml (.puml) -> PlantUML server -> PNG
# - UML package diagram: pydeps (.dot) -> QuickChart Graphviz -> PNG
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

.PHONY: doc-deps doc uml docs serve-doc clean-doc

# Install Python-only deps (works on macOS & Windows)
doc-deps: venv
	"$(PIP)" install -U pdoc py2puml pydeps requests
	@echo "✓ Installed: pdoc, py2puml, pydeps, requests"

# Generate HTML API docs from Python docstrings -> doc/api
# Use --search-path so imports like 'from dice import Dice' resolve without PYTHONPATH tweaks.
doc: venv
	@mkdir -p "doc/api"
	"$(PY)" -c "import sys, runpy, importlib.util; sys.path.insert(0, r'src'); sys.argv=['pdoc','-o', r'doc/api','--docformat','google','--no-show-source', r'src']; m='pdoc.__main__'; runpy.run_module(m if importlib.util.find_spec(m) else 'pdoc', run_name='__main__'); print('✓ API documentation: doc/api/index.html')"

# Generate UML diagrams as PNGs into doc/uml (no Graphviz, no pyreverse)
uml: venv
	@mkdir -p "$(UML_DIR)"
	@echo "• Building class diagram (.puml via py2puml) ..."
	"$(PY)" -m $(PY2PUML_MOD) "$(SRC_ABS)" "$(UML_DIR)/classes_$(PROJECT).puml"
	@echo "• Rendering class diagram to PNG via PlantUML server ..."
	"$(PY)" -c "import requests, pathlib; p=pathlib.Path(r'$(UML_DIR)/classes_$(PROJECT).puml'); png=p.with_suffix(p.suffix + '.png'); r=requests.post('https://www.planttext.com/api/plantuml/png', files={'file': ('classes.puml', p.read_bytes())}); r.raise_for_status(); png.write_bytes(r.content); print('✓ Class diagram PNG:', png)"
	@echo "• Building package dependency DOT via pydeps ..."
	"$(PY)" -m $(PYDEPS_CMD) --noshow --no-output --show-dot --dot-output "$(UML_DIR)/packages_$(PROJECT).dot" "$(SRC_ABS)"
	@echo "• Rendering package diagram DOT -> PNG via QuickChart Graphviz ..."
	"$(PY)" -c "import json, requests, pathlib; f=pathlib.Path(r'$(UML_DIR)/packages_$(PROJECT).dot'); png=f.with_suffix('.png'); r=requests.post('https://quickchart.io/graphviz', json={'graph': f.read_text(encoding='utf-8'), 'layout': 'dot', 'format': 'png'}); r.raise_for_status(); png.write_bytes(r.content); print('✓ Package diagram PNG:', png)"
	@echo "✓ UML generated in: $(UML_DIR)"

# Build both API docs and UML PNGs
docs: doc uml
	@echo "✓ Full documentation written to: $(DOC_DIR)/"

# Serve API docs locally (http://127.0.0.1:8080)
serve-doc: venv
	"$(PY)" -m $(PDOC_MOD) --http :8080 "$(SRC)"

# Clean only generated documentation
clean-doc:
	@rm -rf "$(API_DIR)" "$(UML_DIR)" || true
	@echo "✓ Documentation cleaned."
