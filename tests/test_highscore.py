from src.highscore import HighScore

def test_load_returns_empty():
    hs = HighScore()
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


