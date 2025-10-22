from src.cheat import Cheat
from src.player import Player
from src import game
from tests.test_game import make_game


def test_cheat_menu_exits_immediately_when_score_is_100():
    '''cheat_menu() should exit immediately if current player's score is 100 or more'''
    g = make_game()
    g.player1 = Player("Player1")
    g.current_player = g.player1
    g.current_player.score = 100
    g.cheats = Cheat(g)
    g.cheats.cheat_menu()
    assert g.current_player.score == 100

def test_show_cheat_menu_runs():
    '''show_cheat_menu() should run without errors'''
    g = make_game()
    g.player1 = Player("Alice")
    g.current_player = g.player1
    g.current_player.score = 42
    cheat = Cheat(g)
    cheat.current = g.current_player
    cheat.show_cheat_menu()

def test_show_cheat_menu_prints_full_menu(capsys):
    """show_cheat_menu() should print menu lines and current points."""
    g = make_game()
    g.player1 = Player("Tester")
    g.current_player = g.player1
    g.current_player.score = 77
    cheat = Cheat(g)
    cheat.current = g.current_player
    cheat.show_cheat_menu()
    out = capsys.readouterr().out

    # Check key menu and the score
    assert "WELCOME TO CHEAT MENU" in out
    assert "- press 1 to add points" in out
    assert "- press 2 to subtract points" in out
    assert "- press 3 to quit the cheat  menu" in out
    assert "Current points: 77" in out

def test_game_is_saved():
    '''Cheat object should store the game passed to it'''
    game = "my_game"
    cheat = Cheat(game)
    assert cheat.game == "my_game"

def test_current_is_none_initially():
    '''Current attribute should be None when Cheat object is created'''
    cheat = Cheat("game")
    assert cheat.current is None

def test_game_can_be_any_object():
    '''Cheat object should accept any object as game'''
    class DummyGame: pass
    g = DummyGame()
    cheat = Cheat(g)
    assert cheat.game is g

def test_multiple_cheat_objects_independent():
    '''Multiple Cheat objects should have independent game attributes'''
    c1 = Cheat("game1")
    c2 = Cheat("game2")
    assert c1.game != c2.game

def test_show_cheat_menu_is_callable():
    '''show_cheat_menu should be a callable method of Cheat'''
    cheat = Cheat("game")
    assert callable(cheat.show_cheat_menu)