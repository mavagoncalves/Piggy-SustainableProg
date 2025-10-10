from src.ai import AI
import pytest

from src.dice import Dice


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
    ai=AI('easy')
    assert ai.easy(10,0,5)=='roll'
