from src.player import Player
def test_initial_values():
    """Player should start with the correct name and 0 score."""
    player = Player("Alice")
    assert player.name == "Alice"
    assert player.score == 0


def test_change_name():
    """Changing name updates the player's name."""
    player = Player("Bob")
    player.change_name("Charlie")
    assert player.name == "Charlie"


def test_add_score_increases_total():
    """Adding points should increase the player's score correctly."""
    player = Player("Dana")
    player.add_score(10)
    assert player.score == 10
    player.add_score(5)
    assert player.score == 15


def test_add_score_does_not_change_name():
    """Adding score should not affect player's name."""
    player = Player("Eli")
    player.add_score(7)
    assert player.name == "Eli"


def test_multiple_players_independent_scores():
    """Each player should track their own score independently."""
    p1 = Player("Anna")
    p2 = Player("Ben")

    p1.add_score(10)
    p2.add_score(5)

    assert p1.score == 10
    assert p2.score == 5
    assert p1.name == "Anna"
    assert p2.name == "Ben"
