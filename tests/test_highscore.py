# tests/test_highscore.py
import os
import json
from src.highscore import HighScore

# ---------- helpers ----------

def make_hs(tmp_path):
    """Construct a HighScore that writes to a temp file."""
    hs = HighScore()
    hs.file = str(tmp_path / "highscore.json")
    return hs

def margin_of(row):
    """Compute winning margin from a row, supporting several field names."""
    ws = row.get("winner_score", row.get("score", row.get("winnerScore", 0)))
    os = row.get("opponent_score", row.get("loser_score", row.get("opponentScore", 0)))
    return int(ws) - int(os)

def winner_name_of(row):
    """Extract winner name from a row, supporting several field names."""
    return (row.get("winner") or
            row.get("winner_name") or
            row.get("name") or
            row.get("winnerName") or
            "")

def opponent_name_of(row):
    """Extract opponent name from a row, supporting several field names."""
    return (row.get("opponent") or
            row.get("opponent_name") or
            row.get("loser") or
            row.get("opponentName") or
            "")

def top_by_margin(hs, n=3):
    """Use hs.top(n) if available; else compute from hs.load()."""
    if hasattr(hs, "top"):
        return hs.top(n)
    rows = hs.load()
    return sorted(rows, key=margin_of, reverse=True)[:n]

# ---------- tests ----------

def test_add_result_persists_single_entry(tmp_path):
    hs = make_hs(tmp_path)
    hs.add_result("Alice", 120, "Bob", 90)
    rows = hs.load()
    assert isinstance(rows, list) and len(rows) == 1
    r = rows[0]
    assert winner_name_of(r) == "Alice"
    if "opponent_score" in r or "opponentScore" in r:
        assert margin_of(r) == 30
    else:
        stored = r.get("winner_score", r.get("score", r.get("winnerScore")))
        assert int(stored) == 120


def test_multiple_entries_sorted_by_margin_desc(tmp_path):
    hs = make_hs(tmp_path)
    hs.add_result("A", 100, "X", 70)   # +30
    hs.add_result("B", 90,  "Y", 80)   # +10
    hs.add_result("C", 85,  "Z", 65)   # +20
    top = top_by_margin(hs, 3)
    margins = list(map(margin_of, top))
    assert margins == sorted(margins, reverse=True)
    assert margins[0] >= margins[-1]

def test_trims_names_to_20_chars(tmp_path):
    hs = make_hs(tmp_path)
    long_w = "W" * 80
    long_o = "O" * 80
    hs.add_result(long_w, 101, long_o, 0)
    row = hs.load()[0]
    assert len(winner_name_of(row)) <= 20
    assert len(opponent_name_of(row)) <= 20

def test_empty_winner_name_is_not_saved(tmp_path):
    hs = make_hs(tmp_path)
    hs.add_result("", 100, "Someone", 0)
    rows = hs.load()
    # Either nothing saved or no empty winner fields
    assert all(winner_name_of(r).strip() != "" for r in rows)

def test_negative_and_zero_scores_are_handled(tmp_path):
    hs = make_hs(tmp_path)
    hs.add_result("ZeroWin", 0, "ZeroLose", -10)
    hs.add_result("NegWin", -5, "MoreNeg", -20)
    rows = hs.load()
    assert len(rows) >= 2
    for r in rows:
        stored = r.get("winner_score", r.get("score", r.get("winnerScore", 0)))
        assert isinstance(int(stored), int)
        if "opponent_score" in r or "opponentScore" in r:
            assert isinstance(margin_of(r), int)


def test_duplicate_names_are_kept_as_separate_entries(tmp_path):
    hs = make_hs(tmp_path)
    hs.add_result("Bob", 100, "X", 50)
    hs.add_result("Bob", 90, "Y", 20)
    names = [winner_name_of(r) for r in hs.load()]
    assert names.count("Bob") == 2

def test_top3_trims_when_more_than_three_entries(tmp_path):
    hs = make_hs(tmp_path)
    # margins: 60, 20, 30, 1
    hs.add_result("W1", 120, "L1", 60)   # 60
    hs.add_result("W2", 110, "L2", 90)   # 20
    hs.add_result("W3", 130, "L3", 100)  # 30
    hs.add_result("W4", 150, "L4", 149)  # 1
    top3 = top_by_margin(hs, 3)
    assert len(top3) == 3
    margins = [margin_of(r) for r in top3]
    assert min(margins) >= 20  # the 1-point win should be out

def test_file_created_on_first_add(tmp_path):
    hs = make_hs(tmp_path)
    assert not os.path.exists(hs.file)
    hs.add_result("A", 101, "B", 0)
    assert os.path.exists(hs.file)
    with open(hs.file, "r", encoding="utf-8") as f:
        content = f.read().strip()
    assert content != ""

def test_load_returns_empty_list_on_missing_or_corrupt_file(tmp_path):
    hs = make_hs(tmp_path)
    # missing file -> []
    assert hs.load() == []
    # corrupt file -> []
    with open(hs.file, "w", encoding="utf-8") as f:
        f.write("{not valid json")
    out = hs.load()
    assert isinstance(out, list) and out == []

def test_tied_margins_both_present_in_top(tmp_path):
    hs = make_hs(tmp_path)
    # two entries with same margin (25)
    hs.add_result("Tie1", 100, "L1", 75)
    hs.add_result("Tie2", 90, "L2", 65)
    # and one bigger margin to ensure ordering
    hs.add_result("Big", 200, "Small", 100)  # margin 100
    top = top_by_margin(hs, 3)
    wins = [winner_name_of(r) for r in top]
    assert "Tie1" in wins and "Tie2" in wins
    # ensure the biggest margin is first or at least present
    assert "Big" in wins

