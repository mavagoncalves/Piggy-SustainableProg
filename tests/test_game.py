
import builtins

from src.game import Game
from src.dice import Dice
from src.highscore import HighScore
from src.cheat import Cheat


# ---------- tiny helpers  ----------

def inpseq(*answers):
    seq = list(answers)
    def _fake_input(_prompt=""):
        if not seq:
            raise RuntimeError("No more inputs left for input()")
        return seq.pop(0)
    return _fake_input


def queue_dice(monkeypatch, rolls):
    """Feed exact dice outcomes; stores last face so face() prints are stable."""
    Dice._test_queue = list(rolls)

    def roll(self):
        if not getattr(Dice, "_test_queue", None):
            raise RuntimeError("Dice queue empty in test")
        val = Dice._test_queue.pop(0)
        setattr(self, "_last_face", val)
        return val

    def face(self):
        return getattr(self, "_last_face", None)

    monkeypatch.setattr(Dice, "roll", roll, raising=True)
    monkeypatch.setattr(Dice, "face", face, raising=True)


def capture_highscore(monkeypatch):
    """Capture HighScore.add_result calls without touching disk."""
    recorded = []
    def add_result(self, *, winner_name, winner_score, opponent_name, opponent_score):
        recorded.append((winner_name, winner_score, opponent_name, opponent_score))
    monkeypatch.setattr(HighScore, "add_result", add_result, raising=True)
    return recorded


# ---------- tests ----------

def test_init_pvp_sets_players_and_current(monkeypatch):
    monkeypatch.setattr(builtins, "input", inpseq("Alice", "1", "Bob"))
    g = Game()
    assert g.game_on is True
    assert g.vs_ai is False
    assert g.current_player is g.player1
    assert g.player1.name == "Alice" and g.player2.name == "Bob"


def test_init_pvai_invalid_difficulty_exits(monkeypatch):
    monkeypatch.setattr(builtins, "input", inpseq("Alice", "2", "insane"))
    g = Game()
    assert g.game_on is False
    assert getattr(g, "ai_controller", None) is None
    assert g.vs_ai is False


def test_init_exit_mode_3(monkeypatch):
    monkeypatch.setattr(builtins, "input", inpseq("Alice", "3"))
    g = Game()
    assert g.game_on is False
    assert g.winner is None


def test_init_invalid_option_exits(monkeypatch):
    monkeypatch.setattr(builtins, "input", inpseq("Alice", "xyz"))
    g = Game()
    assert g.game_on is False


def test_plays_turn_quit_ends_game(monkeypatch, capsys):
    monkeypatch.setattr(builtins, "input", inpseq("Alice", "1", "Bob"))
    g = Game()
    monkeypatch.setattr(builtins, "input", inpseq("q"))
    g.plays_turn()
    out = capsys.readouterr().out
    assert "Game ended without winner!" in out
    assert g.game_on is False
    assert g.round_score == 0


def test_hold_with_zero_points_then_quit(monkeypatch, capsys):
    monkeypatch.setattr(builtins, "input", inpseq("Alice", "1", "Bob"))
    g = Game()
    monkeypatch.setattr(builtins, "input", inpseq("h", "q"))
    g.plays_turn()
    out = capsys.readouterr().out
    assert "You can't hold 0 points" in out
    assert g.game_on is False
    assert g.round_score == 0


def test_roll_one_loses_turn_keeps_game_on(monkeypatch):
    queue_dice(monkeypatch, [1])
    monkeypatch.setattr(builtins, "input", inpseq("Alice", "1", "Bob"))
    g = Game()
    monkeypatch.setattr(builtins, "input", inpseq("r"))
    g.plays_turn()
    assert g.game_on is True            # only loses the turn
    assert g.round_score == 0


def test_accumulate_then_hold_hits_100_and_saves_highscore(monkeypatch):
    queue_dice(monkeypatch, [3, 2])     # +5 this turn
    recorded = capture_highscore(monkeypatch)
    monkeypatch.setattr(builtins, "input", inpseq("Alice", "1", "Bob"))
    g = Game()
    g.player1.score = 95                # 95 + 5 = 100
    monkeypatch.setattr(builtins, "input", inpseq("r", "r", "h"))
    g.plays_turn()
    assert g.game_on is False
    assert len(recorded) == 1
    winner, wscore, opp, oscore = recorded[0]
    assert winner == "Alice"
    assert wscore == 100
    assert opp == "Bob" and oscore == 0


def test_hidden_command_triggers_cheat_menu(monkeypatch):
    calls = {"n": 0}
    def fake_cheat_menu(self):  # patch real Cheat.cheat_menu
        calls["n"] += 1
    monkeypatch.setattr(Cheat, "cheat_menu", fake_cheat_menu, raising=True)

    monkeypatch.setattr(builtins, "input", inpseq("Alice", "1", "Bob"))
    g = Game()
    monkeypatch.setattr(builtins, "input", inpseq("hidden", "q"))
    g.plays_turn()
    assert calls["n"] == 1
    assert g.game_on is False


def test_invalid_choice_message_then_quit(monkeypatch, capsys):
    monkeypatch.setattr(builtins, "input", inpseq("Alice", "1", "Bob"))
    g = Game()
    monkeypatch.setattr(builtins, "input", inpseq("x", "q"))
    g.plays_turn()
    out = capsys.readouterr().out
    assert "Invalid choice" in out
    assert g.game_on is False


def test_ai_turn_roll_one_loses_immediately(monkeypatch, capsys):
    queue_dice(monkeypatch, [1])
    monkeypatch.setattr(builtins, "input", inpseq("Alice", "2", "easy"))
    g = Game()
    g.current_player = g.player2
    g.ai_turn()
    out = capsys.readouterr().out
    assert "lost the score and the turn!" in out
    assert g.round_score == 0
    assert g.game_on is True


def test_ai_turn_hold_adds_and_winning_does_not_save_highscore(monkeypatch):
    queue_dice(monkeypatch, [6])
    recorded = capture_highscore(monkeypatch)
    monkeypatch.setattr(builtins, "input", inpseq("Alice", "2", "hard"))
    g = Game()
    g.current_player = g.player2
    g.player2.is_ai = True
    g.player2.add_score(95)             # 95 + 6 = 101

    # force AI to 'hold'
    def hold_decide(*_a, **_k): return "hold"
    monkeypatch.setattr(g.ai_controller, "decide_difficulty", hold_decide, raising=True)

    g.ai_turn()
    assert g.game_on is False
    assert recorded == []               # AI wins -> not saved


def test_change_player_toggles_between_p1_and_p2(monkeypatch):
    monkeypatch.setattr(builtins, "input", inpseq("Alice", "1", "Bob"))
    g = Game()
    assert g.current_player is g.player1
    g.change_player()
    assert g.current_player is g.player2
    g.change_player()
    assert g.current_player is g.player1


def test_run_plays_turn_then_switches_then_quits(monkeypatch):
    queue_dice(monkeypatch, [1])        # first player will roll 1 and lose turn
    monkeypatch.setattr(builtins, "input", inpseq("Alice", "1", "Bob"))
    g = Game()
    monkeypatch.setattr(builtins, "input", inpseq("r", "q"))  # r -> 1; then q on next player's turn
    g.run()
    assert g.game_on is False
    assert g.current_player in (g.player1, g.player2)


def test_check_score_false_when_under_100(monkeypatch):
    monkeypatch.setattr(builtins, "input", inpseq("Alice", "1", "Bob"))
    g = Game()
    g.player1.score = 99
    g.current_player = g.player1
    assert g.check_score() is False
    assert g.game_on is True
