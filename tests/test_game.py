from src.game import Game


class FakePlayer:
    def __init__(self, name):
        self.name = name
        self.score = 0
    def add_score(self, points):
        self.score += points

class FakeDice:
    def __init__(self, sides=6, sequence=None):
        self.sequence = list(sequence) if sequence else [6]
    def roll(self):
        if self.sequence:
            val = self.sequence.pop(0)
            self._last = val
            return val
        return getattr(self, "_last", 6)
    def face(self):
        return "⚅"

class FakeAI:
    def __init__(self, decisions):
        self.decisions = list(decisions)
    def decide_difficulty(self, my, opp, round_score):
        if self.decisions:
            return self.decisions.pop(0)
        return "hold"

class TestGame(game.Game):
    def __init__(self):
        pass