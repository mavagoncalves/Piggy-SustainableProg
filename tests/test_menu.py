from src.menu import Menu
from unittest.mock import patch
import pytest


    #   Command for Windows
    #   $env:PYTHONPATH="."; .venv\Scripts\pytest.exe -v


def test_menu_just_runs():
    menu=Menu()
    menu.display()

def test_shows_rules():
    menu=Menu()
    menu.rules()

def test_menu_string_input_is_invalid():
    menu=Menu()
    with patch("builtins.input", side_effect=["r","5"]):
        # "r" as invalid, gets the invalid input, and gets back
        # "5" to get out of the loop
        menu.run()

def test_menu_int_input_not_recognized():
    menu=Menu()
    with patch("builtins.input", side_effect=[1,"5"]):
        # same as previous
        menu.run()