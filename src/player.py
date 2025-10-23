'''Player module defining the Player class'''
class Player:
    '''Player class to represent a game player
    Attributes:
    - name: String representing the player's name
    - score: Integer representing the player's current score
    '''
    def __init__(self, name):
        self.name = name
        self.score = 0

    def change_name(self, new_name):
        '''Changes the player's name'''
        self.name = new_name
        print(f"Name changed to {self.name}")

    def add_score(self, points):
        '''Adds points to the player's score'''
        self.score += points
        print(f"{self.name} gained {points} points. Total score: {self.score}")
