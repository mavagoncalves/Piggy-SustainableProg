import builtins

from src import game

from src.player import Player
import pytest

def make_game():
    return game.Game.__new__(game.Game)

def test_change_player_switches_between_players():
    '''change_player() should switch current_player between player1 and player2'''
    g = make_game()
    g.player1 = Player("Player1")
    g.player2 = Player("Player2")
    g.current_player = g.player1
    g.change_player()
    assert g.current_player is g.player2
    g.change_player()
    assert g.current_player is g.player1

def test_check_score_sets_game_over_when_at_least_100():
    g = make_game()
    g.player1 = Player("P1"); g.player1.score = 100
    g.player2 = Player("P2"); g.player2.score = 70
    g.current_player = g.player1

    assert g.check_score() is True
    assert g.game_on is False  # game stops on win

def test_check_score_returns_false_below_100():
    g = make_game()
    g.player1 = Player("P1"); g.player1.score = 99
    g.player2 = Player("P2"); g.player2.score = 0
    g.current_player = g.player1

    assert g.check_score() is False
    assert g.game_on is True

def test_check_score_also_triggers_when_above_100():
    g = make_game()
    g.player1 = Player("Alice"); g.player1.score = 30
    g.player2 = Player("Bob");   g.player2.score = 150
    g.current_player = g.player2

    assert g.check_score() is True
    assert g.game_on is False

def test_check_score_returns_false_below_100():
    '''check_score() should return False if score is below 100 and not set winner'''
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

def test_change_player_from_player2_goes_back_to_player1():
    """If it's player2's turn, change_player() should switch to player1."""
    g = make_game()
    g.player1 = Player("P1")
    g.player2 = Player("P2")
    g.current_player = g.player2
    g.change_player()
    assert g.current_player is g.player1


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

@pytest.mark.parametrize("ai_name", ["AI", "ai", "Ai", "aI"])
def test_check_score_ai_wins_by_name_variants_stop_game(ai_name):
    """
    If the current player is 'AI', check_score() must:
    - return True
    - set game_on to False
    - not require any user input
    """
    g = make_game()
    g.player1 = Player("Human"); g.player1.score = 12
    g.player2 = Player(ai_name); g.player2.score = 100
    g.current_player = g.player2
    g.game_on = True

    assert g.check_score() is True
    assert g.game_on is False

def test_check_score_returns_false_just_below_100_no_side_effects():
    """
    Below 100 must return False and keep game running; no winner or score changes.
    """
    g = make_game()
    g.player1 = Player("Alice"); g.player1.score = 99
    g.player2 = Player("Bob");   g.player2.score = 80
    g.current_player = g.player1
    g.game_on = True

    assert g.check_score() is False
    assert g.game_on is True

    assert g.player1.score == 99
    assert g.player2.score == 80

def test_change_player_from_none_defaults_to_player1():
    g = make_game()
    g.player1 = Player("A")
    g.player2 = Player("B")
    g.current_player = None

    g.change_player()
    assert g.current_player is g.player1

def test_run_returns_immediately_if_game_off():
    g = make_game()
    g.game_on = False
    g.winner = None
    # Should be a no-op and not raise
    g.run()
    assert g.game_on is False
    assert g.winner is None

class FakeDice:
    """Deterministic dice: provide a list of ints to yield in order."""
    def __init__(self, rolls):
        self._rolls = list(rolls)
        self.value = None

    def roll(self):
        if not self._rolls:
            raise AssertionError("FakeDice ran out of rolls")
        self.value = self._rolls.pop(0)
        return self.value

    def face(self):
        faces = {1:"⚀",2:"⚁",3:"⚂",4:"⚃",5:"⚄",6:"⚅"}
        return faces.get(self.value, "?")


class FakeAI:
    """Return the next decision ('roll' or 'hold') each time."""
    def __init__(self, decisions):
        self._decisions = list(decisions)

    def decide_difficulty(self, my, op, turn):
        if not self._decisions:
            raise AssertionError("FakeAI ran out of decisions")
        return self._decisions.pop(0)


class SpyHighScore:
    """Intercept add_result() calls; don't write files."""
    def __init__(self):
        self.calls = []

    def add_result(self, **kw):
        self.calls.append(kw)


def make_game_bare():
    return game.Game.__new__(game.Game)

def test_init_pvp_sets_players_and_current(monkeypatch):
    # Inputs: p1 name, mode=1, p2 name
    inputs = iter(["Alice", "1", "Bob"])
    monkeypatch.setattr(builtins, "input", lambda *_: next(inputs))

    g = game.Game()  # run __init__

    assert isinstance(g.player1, Player) and g.player1.name == "Alice"
    assert isinstance(g.player2, Player) and g.player2.name == "Bob"
    assert g.current_player is g.player1
    assert g.vs_ai is False
    assert g.game_on is True

def test_init_pvai_valid_difficulty(monkeypatch):

    inputs = iter(["A", "2", "medium"])
    monkeypatch.setattr(builtins, "input", lambda *_: next(inputs))

    g = game.Game()

    assert g.vs_ai is True
    assert g.current_player is g.player1
    assert g.player2.name == "AI"
    assert g.ai_controller is not None
    assert g.game_on is True

def test_init_exit_option(monkeypatch, capsys):
    inputs = iter(["A", "3"])
    monkeypatch.setattr(builtins, "input", lambda *_: next(inputs))

    g = game.Game()

    assert g.game_on is False
    assert g.current_player is None
    out = capsys.readouterr().out
    assert "Exiting..." in out

def test_init_invalid_menu_option(monkeypatch, capsys):
    inputs = iter(["A", "9"])
    monkeypatch.setattr(builtins, "input", lambda *_: next(inputs))

    g = game.Game()

    assert g.game_on is False
    out = capsys.readouterr().out
    assert "Invalid option" in out

def test_run_calls_turn_then_stops_when_winner_set(monkeypatch):
    g = make_game_bare()
    g.player1 = Player("A"); g.player2 = Player("B")
    g.current_player = g.player1
    g.game_on = True
    g.winner = None

    calls = {"turns": 0, "switches": 0}

    def fake_plays_turn():
        calls["turns"] += 1
        g.winner = g.current_player

    def fake_change_player():
        calls["switches"] += 1
        g.current_player = g.player2 if g.current_player is g.player1 else g.player1

    monkeypatch.setattr(g, "plays_turn", fake_plays_turn)
    monkeypatch.setattr(g, "change_player", fake_change_player)

    g.run()

    assert calls["turns"] == 1
    assert calls["switches"] == 0
    assert g.winner is g.player1


def test_init_invalid_difficulty_stops_game():
    """When invalid AI difficulty is entered, game_on should be False."""
    from unittest.mock import patch

    with patch('builtins.input', side_effect=['TestPlayer', '2', 'invalid']):
        g = game.Game()

    assert g.game_on is False
    assert g.player1.name == 'TestPlayer'


def test_plays_turn_exits_immediately_when_game_off():
    """plays_turn() should return immediately if game_on is False."""
    from unittest.mock import patch
    g = make_game()
    g.game_on = False
    g.current_player = Player("Test")
    g.round_score = 99

    with patch('builtins.input') as mock_input:
        g.plays_turn()

    mock_input.assert_not_called()
    assert g.round_score == 99


def test_plays_turn_calls_ai_turn_for_ai_player():
    """When vs_ai is True and current player is player2, should call ai_turn()."""
    from unittest.mock import patch, Mock
    g = make_game()
    g.player1 = Player("Human")
    g.player2 = Player("AI")
    g.current_player = g.player2
    g.vs_ai = True
    g.game_on = True
    g.ai_turn = Mock()

    with patch('builtins.print'):
        g.plays_turn()

    g.ai_turn.assert_called_once()



