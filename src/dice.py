'''Dice module for Piggy game'''
import random

class Dice:
    '''Dice class to simulate a dice roll
    Attributes:
    - sides: Integer indicating the number of sides on the dice
    - value: Integer indicating the current value of the dice
    - icon: String representing the visual icon of the dice face
    '''
    def __init__(self):
        self.value=random.randint(1, 6)
        self.icon=None

    def roll(self):
        '''Rolls the dice and updates its value and icon'''
        self.value=random.randint(1, 6)
        self.icon=self.face()
        return self.value

    def face(self): #This assigns the icon according the dice's value
        '''Returns the icon corresponding to the dice's value'''
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
        '''Returns a string showing the dice face and its value'''
        print(f"Result: {self.face()} -> {self.value}")
