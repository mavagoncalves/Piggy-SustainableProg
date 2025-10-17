from src import game

from src.player import Player


class TestGame(game.Game):
    def __init__(self):
        super().__init__()

def test_change_player_switches_between_players():
    g = TestGame()
    g.player1 = Player("Player1")
    g.player2 = Player("Player2")
    g.current_player = g.player1
    g.change_player()
    assert g.current_player is g.player2
    g.change_player()
    assert g.current_player is g.player1








