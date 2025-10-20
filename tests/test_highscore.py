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

