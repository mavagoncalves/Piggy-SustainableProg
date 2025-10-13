from src.ai import AI
import pytest
import random

#   $env:PYTHONPATH="."; .venv\Scripts\pytest.exe -v
#EASY
def test_easy_returns_hold_when_goal():
    ai=AI('easy', goal=100)
    assert ai.easy(95,0,5)=='hold'

def test_easy_holds_when_goal_surpassed():
    ai=AI('easy', goal=100)
    assert ai.easy(97,0,6)=='hold'

def test_easy_holds_when_limit():
    ai=AI('easy')
    assert ai.easy(10,0,20) =='hold'

def test_easy_returns_roll_when_not_finished():
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
    ai=AI('medium', goal=100)
    assert ai.medium(95,0,5)=='hold'

def test_medium_holds_when_goal_surpassed():
    ai=AI('medium', goal=100)
    assert ai.medium(97,0,6)=='hold'

def test_medium_holds_when_limit():
    ai=AI('medium', goal = 100)
    assert ai.medium(10,0,20)=='hold'

def test_medium_returns_roll_when_not_finished():
    ai=AI('medium', goal = 100)
    myscore = 10
    opponentscore = 0
    turn_score = 10
    assert myscore + turn_score < ai.goal
    assert turn_score < 20
    assert ai.medium(myscore, opponentscore, turn_score) == 'roll'


#HARD
def test_hard_holds_when_goal():
    ai=AI('hard', goal=100)
    assert ai.hard(95,0,5)=='hold'

def test_hard_holds_when_goal_surpassed():
    ai=AI('hard', goal=100)
    assert ai.hard(97,0,6)=='hold'