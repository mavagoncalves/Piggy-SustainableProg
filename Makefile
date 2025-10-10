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
