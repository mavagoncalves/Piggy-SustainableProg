from src.highscore import HighScore

def test_load_returns_empty():
    hs = HighScore()
    assert hs.load() == []