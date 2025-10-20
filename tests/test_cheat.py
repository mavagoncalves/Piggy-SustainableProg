from src.cheat import Cheat
from src.player import Player
from src import game
from tests.test_game import make_game


def test_cheat_menu_exits_immediately_when_score_is_100():
     g = make_game()
     g.player1 = Player("Player1")
     g.current_player = g.player1
     g.current_player.score = 100
     g.cheats = Cheat(g)
     g.cheats.cheat_menu()
     assert g.current_player.score == 100

def test_show_cheat_menu_runs():
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
    game = "my_game"
    cheat = Cheat(game)
    assert cheat.game == "my_game"

def test_current_is_none_initially():
    cheat = Cheat("game")
    assert cheat.current is None

def test_game_can_be_any_object():
    class DummyGame: pass
    g = DummyGame()
    cheat = Cheat(g)
    assert cheat.game is g