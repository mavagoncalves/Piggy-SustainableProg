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

# Check that face() shows the right symbol
def test_face_matches_value():
    d = Dice(6)
    d.value = 3
    assert d.face() == "⚂"