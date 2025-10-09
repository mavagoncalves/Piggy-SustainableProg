from src.dice import Dice

# Checks that the roll function returns a value within the specified range
def test_roll_in_range():
    d = Dice(6)
    value = d.roll()
    assert 1 <= value <= 6

# Check that the roll returns an int
def test_roll_is_int():
    d = Dice(6)
    value = d.roll()
    assert type(value) == int

