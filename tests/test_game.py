from src import game

from src.player import Player


class TestGame(game.Game):
    def __init__(self):
        pass

def test_change_player_switches_between_players():
    g = TestGame()
    g.player1 = Player("Player1")
    g.player2 = Player("Player2")
    g.current_player = g.player1
    g.change_player()
    assert g.current_player is g.player2
    g.change_player()
    assert g.current_player is g.player1

def test_check_score_sets_winner_at_or_above_100():
    g = TestGame()
    g.player1 = Player("Player1")
    g.player2 = Player("Player2")
    g.current_player = g.player1
    g.winner = None
    g.current_player.score = 100
    assert g.check_score() is True
    assert g.winner is g.current_player

def test_check_score_returns_false_below_100():
    g = TestGame()
    g.player1 = Player("Player1")
    g.player2 = Player("Player2")
    g.current_player = g.player1
    g.winner = None
    g.current_player.score = 99
    assert g.check_score() is False
    assert g.winner is None

def test_cheat_menu_exits_immediately_when_score_is_100():
    g = TestGame()
    g.player1 = Player("Player1")
    g.current_player = g.player1
    g.current_player.score = 100
    g.cheat_menu()
    assert g.current_player.score == 100

def test_show_cheat_menu_runs():
    g = TestGame()
    g.player1 = Player("Alice")
    g.current_player = g.player1
    g.current_player.score = 42
    g.show_cheat_menu()







