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

# def test_cheat_menu_exits_immediately_when_score_is_100():
#     g = make_game()
#     g.player1 = Player("Player1")
#     g.current_player = g.player1
#     g.current_player.score = 100
#     g.cheat_menu()
#     assert g.current_player.score == 100
#
# def test_show_cheat_menu_runs():
#     g = make_game()
#     g.player1 = Player("Alice")
#     g.current_player = g.player1
#     g.current_player.score = 42
#     g.show_cheat_menu()

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

# def test_show_cheat_menu_prints_full_menu(capsys):
#     """show_cheat_menu() should print menu lines and current points."""
#     g = make_game()
#     g.player1 = Player("Tester")
#     g.current_player = g.player1
#     g.current_player.score = 77
#
#     g.show_cheat_menu()
#     out = capsys.readouterr().out
#
#     # Check key menu and the score
#     assert "WELCOME TO CHEAT MENU" in out
#     assert "- press 1 to add points" in out
#     assert "- press 2 to subtract points" in out
#     assert "- press 3 to quit the cheat  menu" in out
#     assert "Current points: 77" in out
