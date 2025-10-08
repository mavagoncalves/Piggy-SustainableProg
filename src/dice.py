import random

class Dice:
    def __init__(self, sides):
        self.value=random.randint(1, 6)
        self.icon=None

    def roll(self):
        self.value=random.randint(1, 6)
        self.icon=self.face
        return self.value

    def face(self):
        icon = {
            1: "⚀",
            2: "⚁",
            3: "⚂",
            4: "⚃",
            5: "⚄",
            6: "⚅"
        }
        return icon[self.value]

    def turn(self):
        print(f"Result: {self.face()} -> {self.value}")