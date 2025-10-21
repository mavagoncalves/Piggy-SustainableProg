
from src.menu import Menu
import pytest

def test_menu_just_runs():
    menu=Menu()
    menu.display()

def test_shows_rules():
    menu=Menu()
    menu.rules()