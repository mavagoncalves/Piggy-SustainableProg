class player:

    def __init__(self, name):
        self.name = name
        self.score = 0

    def change_name(self, new_name):
        self.name = new_name
        print(f"Name changed to {self.name}")

    def add_score(self, points):
        self.score += points
        print(f"{self.name} gained {points} points. Total score: {self.score}")

