import random

class AI:
    def __init__(self, difficulty, goal=100):
        self.difficulty = difficulty.lower()
        self.goal = goal

    def decide_difficulty(self, myscore, opponent_score, turn_score):
        if self.difficulty == 'easy':
            return self.easy(myscore, opponent_score, turn_score)
        elif self.difficulty == 'medium':
            return self.medium(myscore, opponent_score, turn_score)
        elif self.difficulty == 'hard':
            return self.hard(myscore, opponent_score, turn_score)
        else:
            raise ValueError("Unknown difficulty level => please choose 'easy', 'medium', or 'hard'.")
    

