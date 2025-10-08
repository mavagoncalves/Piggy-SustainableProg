import random

class Dice:
    def __init__(self, sides):
        self.value=random.randint(1, 6)
        self.icon=None

    def roll(self):
        self.value=random.randint(1, 6)
        self.icon=self.face
        return self.value

