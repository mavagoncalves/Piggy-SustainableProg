from src import game

from src.player import Player


def make_game():
    return game.Game.__new__(game.Game)

def test_change_player_switches_between_players():
    g = make_game()
    g.player1 = Player("Player1")
    g.player2 = Player("Player2")
    g.current_player = g.player1
    g.change_player()
    assert g.current_player is g.player2
    g.change_player()
    assert g.current_player is g.player1

def test_check_score_sets_winner_at_or_above_100():
    g = make_game()
    g.player1 = Player("Player1")
    g.player2 = Player("Player2")
    g.current_player = g.player1
    g.winner = None
    g.current_player.score = 100
    assert g.check_score() is True
    assert g.winner is g.current_player

def test_check_score_returns_false_below_100():
    g = make_game()
    g.player1 = Player("Player1")
    g.player2 = Player("Player2")
    g.current_player = g.player1
    g.winner = None
    g.current_player.score = 99
    assert g.check_score() is False
    assert g.winner is None

def test_change_player_from_none_sets_player1():
    """If current_player is None, change_player should default to player1."""
    g = make_game()
    g.player1 = Player("P1")
    g.player2 = Player("P2")
    g.current_player = None
    g.change_player()
    assert g.current_player is g.player1

def test_run_returns_immediately_when_game_off():
    """run() should exit right away if game_on is False (no loops, no errors)."""
    g = make_game()
    g.game_on = False
    g.winner = None
    # Should not raise and should not modify winner
    g.run()
    assert g.game_on is False
    assert g.winner is None

def test_winner_persists_after_player_change():
    """Once a winner is set, changing the current player shouldn't affect winner."""
    g = make_game()
    g.player1 = Player("Alice")
    g.player2 = Player("Bob")
    g.current_player = g.player1
    g.winner = g.player1
    g.change_player()
    assert g.current_player is g.player2
    assert g.winner is g.player1  # winner remains the same

def test_check_score_does_not_clear_existing_winner_on_other_turn():
    """
    After one player wins, calling check_score for the other player (below 100)
    should return False and keep the original winner intact.
    """
    g = make_game()
    g.player1 = Player("A"); g.player1.score = 120
    g.player2 = Player("B"); g.player2.score = 50
    g.current_player = g.player1
    assert g.check_score() is True
    assert g.winner is g.player1

    # Switch to the other player and verify winner doesn't change
    g.current_player = g.player2
    assert g.check_score() is False
    assert g.winner is g.player1

def test_change_player_from_player2_goes_back_to_player1():
    """If it's player2's turn, change_player() should switch to player1."""
    g = make_game()
    g.player1 = Player("P1")
    g.player2 = Player("P2")
    g.current_player = g.player2
    g.change_player()
    assert g.current_player is g.player1

def test_check_score_above_100_sets_winner_and_returns_true():
    """Scores strictly above 100 should also declare a winner."""
    g = make_game()
    g.player1 = Player("Alice")
    g.player2 = Player("Bob")
    g.current_player = g.player2
    g.current_player.score = 150
    g.winner = None
    assert g.check_score() is True
    assert g.winner is g.player2
    assert g.winner.name == "Bob"
    assert g.winner.score == 150