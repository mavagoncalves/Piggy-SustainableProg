from src.menu import Menu
from unittest.mock import patch
import pytest

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