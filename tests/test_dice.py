from src.dice import Dice

# Checks that the roll function returns a value within the specified range
def test_roll_in_range():
    '''Tests that the roll() method returns a value between 1 and 6'''
    d = Dice()
    value = d.roll()
    assert 1 <= value <= 6

# Check that the roll returns an int
def test_roll_is_int():
    '''Tests that the roll() method returns an integer'''
    d = Dice()
    value = d.roll()
    assert type(value) == int

# Check that face() shows the right symbol
def test_face_matches_value():
    '''Tests that the face() method returns the correct icon for the dice value'''
    d = Dice()
    d.value = 3
    assert d.face() == "⚂"

# Check that the face updates after rolling
def test_face_updates():
    '''Tests that the icon attribute is updated after rolling the dice'''
    d = Dice()
    d.roll()
    possible_icons = ["⚀", "⚁", "⚂", "⚃", "⚄", "⚅"]
    assert d.icon in possible_icons