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