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