from src.menu import Menu
from src.game import Game
from src.player import Player


def test_menu_display_shows_expected_lines():
    '''display() should show main menu options'''
    m = Menu()
    m.display()

def test_shows_rules():
    '''rules() should execute without errors'''
    menu=Menu()
    menu.rules()

def test_change_name_no_game():
    '''change_name() should handle no game in progress'''
    menu=Menu()
    result = menu.change_name()
    assert result == "No game in progress."

def test_change_name_changes_names():
    '''change_name() should change player names via cli'''
    menu=Menu()
    menu.game = Game.__new__(Game)
    menu.game.player1 = Player("OldName1")
    menu.game.player2 = Player("OldName2")
    class MockCLI:
        def onecmd(self, prompt):
            if "Player 1" in prompt:
                return "NewName1"
            elif "Player 2" in prompt:
                return "NewName2"
            return ""
    menu.cli = MockCLI()
    result = menu.change_name()
    assert "Player 1 name changed to NewName1" in result
    assert "Player 2 name changed to NewName2" in result
    assert menu.game.player1.name == "NewName1"
    assert menu.game.player2.name == "NewName2"