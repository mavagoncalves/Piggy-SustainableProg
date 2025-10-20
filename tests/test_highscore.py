from src.highscore import HighScore
import os

def test_load_returns_empty():
    hs = HighScore()
    if os.path.exists(hs.file):
        os.remove(hs.file)
    assert hs.load() == []

def test_save_and_load():
    hs = HighScore()
    data = [["Alice", 100]]
    hs.save(data)
    result = hs.load()
    assert result == data

def test_add_ignores_empty_name():
    hs = HighScore()
    hs.save([])
    hs.add("", 50)
    assert hs.load() == []

def test_add_casts_to_int():
    hs = HighScore()
    hs.save([])
    hs.add("Alice", "50")
    result = hs.top()
    assert result == [{"name": "Alice", "score": 50}]

def test_keeps_only_top_three():
    hs = HighScore()
    hs.save([])
    hs.add("Alice", 10)
    hs.add("Bob", 20)
    hs.add("Charlie", 30)
    hs.add("Daniel", 40)
    top = hs.top()
    assert len(top) == 3
    assert top[0]["score"] == 40

def test_new_lower_score_goes_to_second_place():
    hs = HighScore()
    hs.save([])
    hs.add("Alice", 100)
    hs.add("Bob", 80)
    top = hs.top()
    assert top[0]["name"] == "Alice"
    assert top[0]["score"] == 100
    assert top[1]["name"] == "Bob"
    assert top[1]["score"] == 80

def test_scores_sorted_descending():
    hs = HighScore()
    hs.save([])
    hs.add("Alice", 5)
    hs.add("Bob", 15)
    hs.add("Charlie", 10)
    top = hs.top()
    assert len(top) == 3
    assert top[0]["name"] == "Bob"
    assert top[1]["name"] == "Charlie"
    assert top[2]["name"] == "Alice"

def test_zero_and_negative_scores():
    hs = HighScore()
    hs.save([])  # reset file
    hs.add("Zero", 0)
    hs.add("Negative", -5)
    hs.add("Positive", 2)
    scores = [s["score"] for s in hs.top()]
    assert scores == [2, 0, -5]

def test_add_same_name_twice():
    hs = HighScore()
    hs.save([])
    hs.add("Bob", 10)
    hs.add("Bob", 20)
    names = [s["name"] for s in hs.top()]
    assert names.count("Bob") >= 1

def test_scores_sorted_even_if_added_unsorted():
    hs = HighScore()
    hs.save([])
    hs.add("Low", 10)
    hs.add("High", 100)
    hs.add("Mid", 50)
    scores = [s["score"] for s in hs.top()]
    assert scores == [100, 50, 10]
