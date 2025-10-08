import random

class Dice:
    def __init__(self, sides):
        self.value=random.randint(1, 6)
        self.icon=None

    def roll(self): #This one will roll an int value from the dice. Call this one to get value.
        self.value=random.randint(1, 6)
        self.icon=self.face
        return self.value

    def face(self): #This assigns the icon according the dice's value
        icon = {
            1: "⚀",
            2: "⚁",
            3: "⚂",
            4: "⚃",
            5: "⚄",
            6: "⚅"
        }
        return icon[self.value]

    def turn(self): #This one joins value + icon. Call this one to show result.
        print(f"Result: {self.face()} -> {self.value}")