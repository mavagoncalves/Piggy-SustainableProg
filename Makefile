# -------------------------------------
# Makefile for Piggy (Dice Game) Project
# Cross-platform (macOS/Linux/Windows)
# -------------------------------------

# -------- Config --------
SRC      ?= src
TESTS    ?= tests
VENV     ?= .venv
COV_MIN  ?= 80
DOC_DIR  ?= doc
API_DIR  ?= $(DOC_DIR)/api
UML_DIR  ?= $(DOC_DIR)/uml
PROJECT  ?= Piggy

PDOC_MOD    := pdoc
PY2PUML_MOD := py2puml
PYDEPS_CMD  := pydeps

# -------- OS-specific shell + paths --------
ifeq ($(OS),Windows_NT)
SHELL := cmd
.SHELLFLAGS := /C
SYS_PY := python
PY  := $(VENV)\Scripts\python.exe
PIP := $(VENV)\Scripts\pip.exe
else
SHELL := /bin/bash
.SHELLFLAGS := -c
SYS_PY := python3
PY  := $(VENV)/bin/python
PIP := $(VENV)/bin/pip
endif

# -------- Phony targets --------
.PHONY: venv install run test clean doc-deps doc uml docs serve-doc clean-doc quality clean-quality diag

# -------- Virtual env (OS-specific) --------
ifeq ($(OS),Windows_NT)
venv:
	if not exist "$(PY)" ( \
		$(SYS_PY) -m venv "$(VENV)" \
	) else ( \
		echo ✓ Virtual environment already exists. \
	)
	"$(PIP)" install -U pip
else
venv:
	[ -x "$(PY)" ] || $(SYS_PY) -m venv "$(VENV)"
	"$(PIP)" install -U pip
endif

# -------- Install deps --------
install: venv
	"$(PIP)" install -r requirements.txt

# -------- Run / Test --------
run: venv
	"$(PY)" main.py

test: venv
	"$(PY)" -m pytest -v

# -------- Clean (portable via Python) --------
clean:
	"$(PY)" -c "import shutil, pathlib; \
[shutil.rmtree(pathlib.Path(p), ignore_errors=True) for p in ['__pycache__','.pytest_cache','htmlcov']]; \
print('✓ Cleaned build/test artifacts')"

# -------- Documentation --------
doc-deps: venv
	"$(PIP)" install -U pdoc py2puml pydeps requests
	@echo "✓ Installed: pdoc, py2puml, pydeps, requests"

doc: venv
	"$(PY)" -c "import os; os.makedirs(r'$(API_DIR)', exist_ok=True)"
	"$(PY)" -c "import sys, runpy, importlib.util; sys.path.insert(0, r'$(SRC)'); \
sys.argv=['pdoc','-o', r'$(API_DIR)','--docformat','google','--no-show-source', r'$(SRC)']; \
m='pdoc.__main__'; runpy.run_module(m if importlib.util.find_spec(m) else 'pdoc', run_name='__main__'); \
print('✓ API documentation: $(API_DIR)/index.html')"

uml: venv
	"$(PY)" -c "import os; os.makedirs(r'$(UML_DIR)', exist_ok=True)"
	"$(PY)" tools/uml_build.py --project "$(PROJECT)" --src "$(SRC)" --out "$(UML_DIR)"

docs: doc uml
	@echo "✓ Full documentation written to: $(DOC_DIR)/"

serve-doc: venv
	"$(PY)" -m $(PDOC_MOD) --http :8080 "$(SRC)"

clean-doc:
	"$(PY)" -c "import shutil; \
shutil.rmtree(r'$(API_DIR)', ignore_errors=True); \
shutil.rmtree(r'$(UML_DIR)', ignore_errors=True); \
print('✓ Documentation cleaned.')"

# -------- Coverage & Lint (cross-platform) --------
quality: venv
	"$(PIP)" install -U pip
	"$(PIP)" install pytest pytest-cov pylint
	@echo "Running pylint..."
	# run inside src so only project files are linted
	@cd "$(SRC)" && "$(PY)" -m pylint --exit-zero --recursive=y .
	@echo "Running tests with coverage (min $(COV_MIN)%)..."
	"$(PY)" -m pytest "$(TESTS)" \
		--maxfail=1 \
		--cov="$(SRC)" \
		--cov-fail-under=$(COV_MIN) \
		--cov-report=term-missing
	@echo "✓ Quality check passed"

clean-quality:
	"$(PY)" -c "import shutil, pathlib; \
shutil.rmtree('.coverage', ignore_errors=True); \
shutil.rmtree('htmlcov', ignore_errors=True); \
shutil.rmtree('.pytest_cache', ignore_errors=True); \
[shutil.rmtree(p, ignore_errors=True) for p in pathlib.Path('$(SRC)').rglob('__pycache__') if p.is_dir()]; \
print('✓ Cleaned quality artifacts')"
