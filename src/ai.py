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
        elif turn_score >= limit:
            return 'hold'
        return 'roll' if random.random() > 0.6 else 'hold'
    
    def medium(self, myscore, opponent_score, turn_score):
        '''
        Medium AI:
        * keep limit at 20
        * if ahead by +20 or more take safer turn (hold at 15)
        * if behind by -30 or more take riskier turn (hold at 25)
        '''

        lead = myscore - opponent_score
        limit = 20

        if myscore + turn_score >= self.goal:
            return 'hold'
        elif lead >= limit:
            limit = 15
        elif lead <= (-30):
            limit = 25
        elif turn_score >= limit:
            return 'hold'
        return 'roll'
    
    def hard(self, myscore, opponent_score, turn_score):
        '''
        Hard AI:
        * adjust limit based on lead/lag
        * addaptive limit based on how close to winning
        '''

        lead = myscore - opponent_score
        limit = 20

        #adjust based on game situation

        if myscore + turn_score >= self.goal:
            return 'hold'
        elif opponent_score >= self.goal - 20:
            limit = 25
        elif myscore >= self.goal - 20:
            limit = min(limit, 15)
        elif lead >= 30:
            limit = 15
        elif lead <= -40:
            limit = 30
        
        #endgame strategy

        need = self.goal - myscore
        if need <= 10:
            if turn_score >= need or turn_score:
                return 'hold'
            return 'roll'
        
        #normal play
        if turn_score >= limit:
            return 'hold'
        return 'roll'


