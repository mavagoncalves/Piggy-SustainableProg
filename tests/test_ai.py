from src.ai import AI
import pytest
import random

#   $env:PYTHONPATH="."; .venv\Scripts\pytest.exe -v
#EASY
def test_easy_returns_hold_when_goal():
    '''Tests that the easy AI holds when reaching or surpassing the goal score'''
    ai=AI('easy', goal=100)
    assert ai.easy(95,0,5)=='hold'

def test_easy_holds_when_goal_surpassed():
    '''Tests that the easy AI holds when surpassing the goal score'''
    ai=AI('easy', goal=100)
    assert ai.easy(97,0,6)=='hold'

def test_easy_holds_when_limit():
    '''Tests that the easy AI holds when reaching the turn score limit'''
    ai=AI('easy')
    assert ai.easy(10,0,20) =='hold'

def test_easy_returns_roll_when_not_finished():
    '''Tests that the easy AI rolls when below the turn score limit and not reaching the goal'''
    ai=AI('easy', goal=100)
    turn_score=10
    myscore=0
    opponentscore=0
    original_random=random.random   #original secured
    try:
        # copy with forced result
        random.random=lambda:0.5
        #And then checks limits
        assert turn_score<20
        assert myscore+turn_score<ai.goal

        assert ai.easy(myscore, opponentscore, turn_score)=='roll'
    finally:
        random.random=original_random
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