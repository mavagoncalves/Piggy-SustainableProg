from src.ai import AI
import pytest
import random

#decide difficulty 
def test_decide_difficulty_easy_dispatch_roll(monkeypatch):
    ai = AI('easy', goal=100)
    # force random.random() < 0.6 so easy path returns 'roll'
    monkeypatch.setattr('random.random', lambda: 0.5)
    assert ai.decide_difficulty(myscore=0, opponent_score=0, turn_score=10) == 'roll'

def test_decide_difficulty_medium_dispatch_hold():
    ai = AI('medium', goal=100)
    # medium holds at 20
    assert ai.decide_difficulty(myscore=10, opponent_score=0, turn_score=20) == 'hold'

def test_decide_difficulty_hard_dispatch_hold():
    ai = AI('hard', goal=100)
    # hard normal rule: holds at >= 20
    assert ai.decide_difficulty(myscore=10, opponent_score=0, turn_score=20) == 'hold'

def test_decide_difficulty_invalid_raises():
    ai = AI('unknown', goal=100)
    with pytest.raises(ValueError) as exc:
        ai.decide_difficulty(0, 0, 0)
    assert "Unknown difficulty level" in str(exc.value)

#EASY
def test_easy_returns_hold_when_goal():
    '''Tests that the easy AI holds when reaching or surpassing the goal score'''
    ai=AI('easy', goal=100)
    assert ai.easy(95,5)=='hold'

def test_easy_holds_when_goal_surpassed():
    '''Tests that the easy AI holds when surpassing the goal score'''
    ai=AI('easy', goal=100)
    assert ai.easy(97,6)=='hold'

def test_easy_holds_when_limit():
    '''Tests that the easy AI holds when reaching the turn score limit'''
    ai=AI('easy')
    assert ai.easy(10,20) =='hold'

def test_easy_returns_roll_when_not_finished():
    '''Tests that the easy AI rolls when below the turn score limit and not reaching the goal'''
    ai=AI('easy', goal=100)
    turn_score=10
    myscore=0
    original_random=random.random   #original secured
    try:
        # copy with forced result
        random.random=lambda:0.5
        #And then checks limits
        assert turn_score<20
        assert myscore+turn_score<ai.goal

        assert ai.easy(myscore, turn_score)=='roll'
    finally:
        random.random=original_random

def test_easy_random_else_branch_hold(monkeypatch):
    ai = AI('EaSy', goal=100)
    # force random.random() >= 0.6 so 'hold'
    monkeypatch.setattr('random.random', lambda: 0.7)
    # below limit, not reaching goal => hit random path -> hold (else branch)
    assert ai.easy(myscore=0, turn_score=10) == 'hold'

#MEDIUM
def test_medium_holds_when_goal():
    '''Tests that the medium AI holds when reaching or surpassing the goal score'''
    ai=AI('medium', goal=100)
    assert ai.medium(95,0,5)=='hold'

def test_medium_holds_when_goal_surpassed():
    '''Tests that the medium AI holds when surpassing the goal score'''
    ai=AI('medium', goal=100)
    assert ai.medium(97,0,6)=='hold'

def test_medium_holds_when_limit():
    '''Tests that the medium AI holds when reaching the turn score limit'''
    ai=AI('medium', goal = 100)
    assert ai.medium(10,0,20)=='hold'

def test_medium_returns_roll_when_not_finished():
    '''Tests that the medium AI rolls when below the turn score limit and not reaching the goal'''
    ai=AI('medium', goal = 100)
    myscore = 10
    opponentscore = 0
    turn_score = 10
    assert myscore + turn_score < ai.goal
    assert turn_score < 20
    assert ai.medium(myscore, opponentscore, turn_score) == 'roll'


#HARD
def test_hard_holds_when_goal():
    '''Tests that the hard AI holds when reaching or surpassing the goal score'''
    ai=AI('hard', goal=100)
    assert ai.hard(95,0,5)=='hold'

def test_hard_holds_when_goal_surpassed():
    '''Tests that the hard AI holds when surpassing the goal score'''
    ai=AI('hard', goal=100)
    assert ai.hard(97,0,6)=='hold'

def test_hard_holds_when_limit():
    '''Tests that the hard AI holds when reaching the turn score limit'''
    ai=AI('hard', goal=100)
    assert ai.hard(10,0,20)=='hold'

def test_hard_returns_roll_when_not_finished():
    '''Tests that the hard AI rolls when below the turn score limit and not reaching the goal'''
    ai=AI('hard', goal=100)
    assert ai.hard(10,0,5)=='roll'

def test_hard_opponent_near_goal_raises_limit_roll():
    """
    opponent_score >= goal - 20 -> limit = max(20, 25) => 25.
    turn_score 24 -> below 25 => roll.
    """
    ai = AI('hard', goal=100)
    assert ai.hard(myscore=10, opponent_score=80, turn_score=24) == 'roll'

def test_hard_self_near_goal_reduces_limit_hold():
    """
    myscore >= goal - 20 -> limit = min(20, 15) => 15.
    turn_score 15 -> hold.
    """
    ai = AI('hard', goal=100)
    assert ai.hard(myscore=85, opponent_score=0, turn_score=15) == 'hold'

def test_hard_big_lead_min_limit_15_hold():
    """
    lead >= 30 -> limit = min(limit, 15).
    With normal base limit 20, becomes 15. turn_score 15 -> hold.
    """
    ai = AI('hard', goal=100)
    assert ai.hard(myscore=60, opponent_score=20, turn_score=15) == 'hold'

def test_hard_big_lag_max_limit_30_roll_then_hold():
    """
    lead <= -40 -> limit = max(limit, 30).
    turn_score 29 -> roll; 30 -> hold.
    """
    ai = AI('hard', goal=100)
    assert ai.hard(myscore=10, opponent_score=60, turn_score=29) == 'roll'
    assert ai.hard(myscore=10, opponent_score=60, turn_score=30) == 'hold'

def test_hard_endgame_need_le_10_roll_and_hold():
    """
    Endgame block: need <= 10.
    turn_score >= min(10, need) -> hold, else roll.
    """
    ai = AI('hard', goal=100)
    # need = 5
    assert ai.hard(myscore=95, opponent_score=0, turn_score=4) == 'roll'
    assert ai.hard(myscore=95, opponent_score=0, turn_score=5) == 'hold'
