import builtins
from src.cheat import Cheat

# ---------- helpers ----------

class DummyPlayer:
    def __init__(self, score=0):
        self.score = score

    def add_score(self, n: int):
        self.score += n


class DummyGame:
    def __init__(self, player: DummyPlayer):
        self.current_player = player


def feed_inputs(monkeypatch, answers):
    """Feed a sequence of answers to builtins.input."""
    it = iter(answers)
    monkeypatch.setattr(builtins, "input", lambda _prompt="": next(it))

# ---------- Tests ----------

def test_invalid_option_then_quit(monkeypatch, capsys):
    """Invalid option prints message, then '3' quits."""
    player = DummyPlayer(score=10)
    game = DummyGame(player)
    cheat = Cheat(game)

    # First give an invalid choice, then quit
    feed_inputs(monkeypatch, ["x", "3"])
    cheat.cheat_menu()
    out = capsys.readouterr().out

    assert "WELCOME TO CHEAT MENU" in out
    assert "Invalid option: please select '1', '2' or '3'." in out
    assert player.score == 10

def test_max_score_exits_without_prompt(capsys):
    """If current score >= 100, it exits immediately and does not show the menu."""
    player = DummyPlayer(score=100)
    game = DummyGame(player)
    cheat = Cheat(game)

    cheat.cheat_menu()
    out = capsys.readouterr().out

    assert "Maximum score reached! Cheat menu will close now" in out
    assert "WELCOME TO CHEAT MENU" not in out


def test_add_points_valid(monkeypatch, capsys):
    """Option 1 with a valid integer in range adds to score and sets cheat_use."""
    player = DummyPlayer(score=10)
    game = DummyGame(player)
    cheat = Cheat(game)

    feed_inputs(monkeypatch, ["1", "5", "3"])  # add 5, then quit
    cheat.cheat_menu()
    out = capsys.readouterr().out

    assert player.score == 15
    assert getattr(player, "cheat_use", False) is True
    assert "WELCOME TO CHEAT MENU" in out


def test_add_points_non_int(monkeypatch, capsys):
    """Option 1 with non-integer input prints error and continues; no score change."""
    player = DummyPlayer(score=7)
    game = DummyGame(player)
    cheat = Cheat(game)

    feed_inputs(monkeypatch, ["1", "abc", "3"])
    cheat.cheat_menu()
    out = capsys.readouterr().out

    assert "Invalid choice, enter a number." in out
    assert player.score == 7
    assert not hasattr(player, "cheat_use")


def test_add_points_out_of_range_low(monkeypatch, capsys):
    """Option 1 with value < 1 prints range error; no score change."""
    player = DummyPlayer(score=12)
    game = DummyGame(player)
    cheat = Cheat(game)

    feed_inputs(monkeypatch, ["1", "0", "3"])
    cheat.cheat_menu()
    out = capsys.readouterr().out

    assert "Invalid choice, enter value between 1-100" in out
    assert player.score == 12


def test_add_points_out_of_range_high(monkeypatch, capsys):
    """Option 1 with value > 100 prints range error; no score change."""
    player = DummyPlayer(score=12)
    game = DummyGame(player)
    cheat = Cheat(game)

    feed_inputs(monkeypatch, ["1", "101", "3"])
    cheat.cheat_menu()
    out = capsys.readouterr().out

    assert "Invalid choice, enter value between 1-100" in out
    assert player.score == 12


def test_subtract_points_non_int(monkeypatch, capsys):
    """Option 2 with non-integer input prints error; no score change."""
    player = DummyPlayer(score=20)
    game = DummyGame(player)
    cheat = Cheat(game)

    feed_inputs(monkeypatch, ["2", "xyz", "3"])
    cheat.cheat_menu()
    out = capsys.readouterr().out

    assert "Invalid choice, enter a number." in out
    assert player.score == 20


def test_subtract_points_out_of_range(monkeypatch, capsys):
    """Option 2 with value < 1 prints range error; no score change."""
    player = DummyPlayer(score=20)
    game = DummyGame(player)
    cheat = Cheat(game)

    feed_inputs(monkeypatch, ["2", "0", "3"])
    cheat.cheat_menu()
    out = capsys.readouterr().out

    assert "Invalid choice, enter value between 1-100" in out
    assert player.score == 20


def test_subtract_points_negative_result(monkeypatch, capsys):
    """Option 2 that would make score negative prints error; no score change."""
    player = DummyPlayer(score=5)
    game = DummyGame(player)
    cheat = Cheat(game)

    feed_inputs(monkeypatch, ["2", "10", "3"])
    cheat.cheat_menu()
    out = capsys.readouterr().out

    assert "your score can't be less than 0" in out
    assert player.score == 5


def test_subtract_points_valid_sets_flag_and_updates(monkeypatch, capsys):
    """Valid subtraction reduces score and sets cheat_use flag."""
    player = DummyPlayer(score=20)
    game = DummyGame(player)
    cheat = Cheat(game)

    feed_inputs(monkeypatch, ["2", "7", "3"])
    cheat.cheat_menu()
    _ = capsys.readouterr().out

    assert player.score == 13
    assert getattr(player, "cheat_use", False) is True
