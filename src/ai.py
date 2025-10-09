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
        
    def easy(self, myscore, opponent_score, turn_score):
        '''
        Easy AI: 
        * rolls until turn score is 20 or more, then holds.
        * holds if it already won.
        * some chance to hold earlier.
        '''
        limit = 20

        if myscore + turn_score >= self.goal:
            return 'hold'
        if turn_score >= limit:
            return 'hold'
        return 'roll' if random.random() > 0.6 else 'hold'
    

