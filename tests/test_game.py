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
    from unittest.mock import patch
    g = make_game()
    g.player1 = Player("Player1")
    g.player2 = Player("Player2")
    g.current_player = g.player1
    g.winner = None
    g.current_player.score = 100

    with patch('builtins.print'), \
            patch('src.game.HighScore'):  # Mock HighScore to avoid file operations
        result = g.check_score()

    assert result is True
    assert g.game_on is False

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

def test_run_exits_immediately_if_winner_already_set():
    """
    When a winner is already set before run(), the loop should not start and
    current_player should remain unchanged.
    """
    g = make_game()
    g.player1 = Player("A")
    g.player2 = Player("B")
    g.current_player = g.player1
    g.winner = g.player2
    g.game_on = True

    g.run()

    assert g.game_on is True
    assert g.current_player is g.player1
    assert g.winner is g.player2

def test_ai_turn_resets_round_score():
    """ai_turn() should start by resetting round_score to 0."""
    from unittest.mock import patch, Mock
    g = make_game()
    g.player1 = Player("Human")
    g.player2 = Player("AI")
    g.current_player = g.player2
    g.vs_ai = True
    g.round_score = 50
    g.ai_controller = Mock()
    g.ai_controller.decide_difficulty.return_value = "hold"
    g.dice = Mock()
    g.dice.roll.return_value = 5
    g.dice.face.return_value = "⚄"
    g.check_score = Mock(return_value=False)

    with patch('builtins.print'):
        g.ai_turn()

    assert g.current_player.score == 5


def test_ai_turn_roll_one_prints_message_and_returns():
    """When AI rolls 1, should print loss message and return immediately."""
    from unittest.mock import patch, Mock
    g = make_game()
    g.player1 = Player("Human")
    g.player2 = Player("AI")
    g.current_player = g.player2
    g.current_player.score = 50
    g.vs_ai = True
    g.ai_controller = Mock()
    g.ai_controller.decide_difficulty.return_value = "roll"
    g.dice = Mock()
    g.dice.roll.return_value = 1
    g.dice.face.return_value = "⚀"

    with patch('builtins.print') as mock_print:
        g.ai_turn()

    print_calls = [str(call) for call in mock_print.call_args_list]
    loss_message_found = any(
        "lost the score and the turn" in str(call).lower()
        for call in print_calls
    )
    assert loss_message_found, "Expected 'lost the score and the turn' message"

    assert g.current_player.score == 50

    assert g.current_player.score == 50

