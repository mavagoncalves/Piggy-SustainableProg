from src.menu import Menu
from unittest.mock import patch


def test_menu_just_runs():
    '''Menu run() should execute without errors'''
    menu=Menu()
    menu.display()

def test_shows_rules():
    '''rules() should execute without errors'''
    menu=Menu()
    menu.rules()

def test_menu_string_input_is_invalid():
    '''menu run() should handle invalid string input'''
    menu=Menu()
    with patch("builtins.input", side_effect=["r","5"]):
        # "r" as invalid, gets the invalid input, and gets back
        # "5" to get out of the loop
        menu.run()

def test_menu_int_input_not_recognized():
    '''menu run() should handle invalid integer input'''
    menu=Menu()
    with patch("builtins.input", side_effect=[1,"5"]):
        # same as previous
        menu.run()

def test_highscore_shown_when_option_4():
    '''menu run() should call HighScore.show() when option 4 is selected'''
    menu=Menu()
    with patch("src.menu.HighScore.show") as mock:
        #puts the show highscore as a mock
        with patch("builtins.input", side_effect=["4","5"]):
            menu.run()
        assert mock.called
        #checks the mock was called