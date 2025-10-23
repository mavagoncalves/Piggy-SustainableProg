import types
import pytest

from src.menu import Menu


# --------- helpers ---------

class MockCLI:
    """Minimal stand-in exposing do_input and recording prompts."""
    def __init__(self, answers):
        self.answers = list(answers)
        self.prompts = []

    def do_input(self, prompt):
        self.prompts.append(prompt)
        return self.answers.pop(0) if self.answers else ""


def make_game(p1="P1", p2="P2"):
    """Create a lightweight game-like object with player1/2 that have 'name' attrs."""
    return types.SimpleNamespace(
        player1=types.SimpleNamespace(name=p1),
        player2=types.SimpleNamespace(name=p2),
    )


# --------- tests for Menu.display ---------

def test_display_includes_all_options_and_order():
    m = Menu()
    out = m.display().splitlines()
    assert out[0] == "=== MAIN MENU ==="
    # ensure key commands are present and in expected order chunk
    expected = [
        "menu: Show this menu",
        "rules: Show game rules",
        "new: Start a new game",
        "change_name: Change player names",
        "highscore: View high scores",
        "score: View current scores",
        "play: Play the game",
        "quit: Exit the game",
    ]
    assert out[1:] == expected
    assert "quit: Exit the game" in out


def test_display_has_no_trailing_blank_lines():
    m = Menu()
    s = m.display()
    assert not s.endswith("\n")
    assert "\n\n" not in s  # no accidental blank line in the middle


# --------- tests for Menu.rules ---------

def test_rules_includes_key_points_and_order():
    m = Menu()
    lines = m.rules().splitlines()
    assert lines[0] == "Rules:"
    assert lines[1].startswith("1.") and "Two players" in lines[1]
    assert lines[2].startswith("2.") and "Reach 100 points" in lines[2]
    assert lines[3].startswith("3.") and "turn total" in lines[3]
    assert lines[4].startswith("4.") and "Roll a 1" in lines[4]
    assert lines[5].startswith("5.") and "Hold" in lines[5]
    assert lines[6].startswith("6.") and "wins" in lines[6]


def test_rules_line_count_looks_reasonable():
    m = Menu()
    lines = m.rules().splitlines()
    assert len(lines) == 7  # "Rules:" + six bullet lines


# --------- tests for Menu.change_name ---------

def test_change_name_no_game():
    m = Menu()
    result = m.change_name()
    assert result == "No game in progress."


def test_change_name_changes_both_names_and_prompts_include_current():
    m = Menu()
    m.game = make_game("Old1", "Old2")
    mock = MockCLI(["New1", "New2"])
    m.cli = mock

    result = m.change_name()

    # assertions about changes
    assert "Player 1 name changed to New1" in result
    assert "Player 2 name changed to New2" in result
    assert m.game.player1.name == "New1"
    assert m.game.player2.name == "New2"
    # assertions about prompts shown to the user
    assert len(mock.prompts) == 2
    assert "Player 1 (Old1)" in mock.prompts[0]
    assert "Player 2 (Old2)" in mock.prompts[1]


def test_change_name_changes_first_only_when_second_empty():
    m = Menu()
    m.game = make_game("A", "B")
    m.cli = MockCLI(["FirstOnly", ""])
    result = m.change_name()
    assert "Player 1 name changed to FirstOnly" in result
    assert "Player 2 name changed" not in result
    assert m.game.player1.name == "FirstOnly"
    assert m.game.player2.name == "B"


def test_change_name_changes_second_only_when_first_empty():
    m = Menu()
    m.game = make_game("A", "B")
    m.cli = MockCLI(["", "SecondOnly"])
    result = m.change_name()
    assert "Player 1 name changed" not in result
    assert "Player 2 name changed to SecondOnly" in result
    assert m.game.player1.name == "A"
    assert m.game.player2.name == "SecondOnly"


def test_change_name_no_names_entered_returns_no_changes():
    m = Menu()
    m.game = make_game("Left", "Right")
    m.cli = MockCLI(["", ""])
    result = m.change_name()
    assert result == "No names changed."
    assert m.game.player1.name == "Left" and m.game.player2.name == "Right"


def test_change_name_strips_whitespace_from_inputs():
    m = Menu()
    m.game = make_game("Alpha", "Beta")
    m.cli = MockCLI(["  NewAlpha  ", " \t NewBeta  "])
    result = m.change_name()
    assert "Player 1 name changed to NewAlpha" in result
    assert "Player 2 name changed to NewBeta" in result
    assert m.game.player1.name == "NewAlpha"
    assert m.game.player2.name == "NewBeta"


def test_change_name_whitespace_only_treated_as_empty():
    m = Menu()
    m.game = make_game("X", "Y")
    m.cli = MockCLI(["   ", "\t  "])
    result = m.change_name()
    assert result == "No names changed."
    assert m.game.player1.name == "X" and m.game.player2.name == "Y"


def test_change_name_prompts_are_exactly_formatted():
    m = Menu()
    m.game = make_game("Ann", "Ben")
    mock = MockCLI(["", ""])
    m.cli = mock
    _ = m.change_name()
    p1, p2 = mock.prompts
    assert p1 == "Enter new name for Player 1 (Ann): "
    assert p2 == "Enter new name for Player 2 (Ben): "
