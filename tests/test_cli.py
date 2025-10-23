import cmd
from src.cli import PiggyCLI, scoreboard_header
from src.menu import Menu
from unittest.mock import Mock, patch
import io


def test_scoreboard_header_with_complete_game():
    """scoreboard_header should display all player info when game has complete data"""
    mock_game = Mock()
    mock_player1 = Mock()
    mock_player1.name = "Player1"
    mock_player1.score = 15
    mock_player2 = Mock()
    mock_player2.name = "Player2"
    mock_player2.score = 25
    mock_current = Mock()
    mock_current.name = "Player1"
    mock_game.player1 = mock_player1
    mock_game.player2 = mock_player2
    mock_game.current_player = mock_current

    with patch('sys.stdout', new_callable=io.StringIO) as mock_stdout:
        scoreboard_header(mock_game)
        output = mock_stdout.getvalue()

    assert "===== SCOREBOARD =====" in output
    assert "Player1: 15" in output
    assert "Player2: 25" in output
    assert "Turn: Player1" in output
    assert "======================" in output


def test_scoreboard_header_with_missing_players():
    """scoreboard_header should handle missing player data gracefully"""
    mock_game = Mock()
    mock_current = Mock()
    mock_current.name = "TestPlayer"
    mock_game.current_player = mock_current

    with patch('sys.stdout', new_callable=io.StringIO) as mock_stdout:
        scoreboard_header(mock_game)
        output = mock_stdout.getvalue()

    assert "===== SCOREBOARD =====" in output
    assert "Turn: TestPlayer" in output
    assert "======================" in output


def test_scoreboard_header_with_no_attributes():
    """scoreboard_header should work with minimal game object"""
    mock_game = Mock()

    with patch('sys.stdout', new_callable=io.StringIO) as mock_stdout:
        scoreboard_header(mock_game)
        output = mock_stdout.getvalue()

    assert "===== SCOREBOARD =====" in output
    assert "======================" in output


def test_piggy_cli_initialization():
    """PiggyCLI should initialize with correct attributes"""
    cli = PiggyCLI()

    assert cli.intro == "Welcome to Piggy! Type 'menu' to see commands."
    assert cli.prompt == "piggy> "
    assert isinstance(cli.menu, Menu)
    assert cli.menu.cli == cli
    assert cli.game is None


def test_bind_game_method():
    """_bind_game should set game and configure UI header"""
    cli = PiggyCLI()
    mock_game = Mock()

    cli._bind_game(mock_game)

    assert cli.game == mock_game
    assert cli.menu.game == mock_game
    assert hasattr(mock_game, 'ui_header')
    assert mock_game.ui_header == scoreboard_header


def test_need_game_without_game():
    """_need_game should return False and print message when no game"""
    cli = PiggyCLI()

    with patch('sys.stdout', new_callable=io.StringIO) as mock_stdout:
        result = cli._need_game()
        output = mock_stdout.getvalue()

    assert result is False
    assert "No game yet. Start one with: new" in output


def test_need_game_with_game():
    """_need_game should return True when game exists"""
    cli = PiggyCLI()
    cli.game = Mock()

    result = cli._need_game()

    assert result is True


def test_do_menu_command():
    """do_menu should display menu options"""
    cli = PiggyCLI()
    cli.menu.display = Mock(return_value="Main Menu Options")

    with patch('sys.stdout', new_callable=io.StringIO) as mock_stdout:
        cli.do_menu("")
        output = mock_stdout.getvalue()

    assert "Main Menu Options" in output
    cli.menu.display.assert_called_once()


def test_do_rules_command():
    """do_rules should display game rules"""
    cli = PiggyCLI()
    cli.menu.rules = Mock(return_value="Game Rules Here")

    with patch('sys.stdout', new_callable=io.StringIO) as mock_stdout:
        cli.do_rules("")
        output = mock_stdout.getvalue()

    assert "Game Rules Here" in output
    cli.menu.rules.assert_called_once()


def test_do_new_command_successful():
    """do_new should create and bind a new game"""
    cli = PiggyCLI()
    mock_game = Mock()
    mock_game.game_on = True

    with patch('src.cli.Game', return_value=mock_game), \
            patch('sys.stdout', new_callable=io.StringIO) as mock_stdout:
        cli.do_new("")
        output = mock_stdout.getvalue()

    assert "Loading Game..." in output
    assert cli.game == mock_game
    assert cli.menu.game == mock_game


def test_do_new_command_failed_game():
    """do_new should handle game that fails to start"""
    cli = PiggyCLI()
    mock_game = Mock()
    mock_game.game_on = False

    with patch('src.cli.Game', return_value=mock_game), \
            patch('sys.stdout', new_callable=io.StringIO) as mock_stdout:
        cli.do_new("")
        output = mock_stdout.getvalue()

    assert "Loading Game..." in output
    assert "Game not started." in output
    assert cli.game is None


def test_do_play_command_without_game():
    """do_play should not run without active game"""
    cli = PiggyCLI()

    with patch('sys.stdout', new_callable=io.StringIO) as mock_stdout:
        cli.do_play("")
        output = mock_stdout.getvalue()

    assert "No game yet. Start one with: new" in output


def test_do_play_command_with_game_no_winner():
    """do_play should run game without winner message"""
    cli = PiggyCLI()
    mock_game = Mock()
    mock_game.winner = None
    cli.game = mock_game

    with patch('sys.stdout', new_callable=io.StringIO):
        cli.do_play("")

    mock_game.run.assert_called_once()


def test_do_play_command_with_winner():
    """do_play should announce winner when game has winner"""
    cli = PiggyCLI()
    mock_game = Mock()
    mock_winner = Mock()
    mock_winner.name = "TestWinner"
    mock_winner.score = 100
    mock_game.winner = mock_winner
    cli.game = mock_game

    with patch('sys.stdout', new_callable=io.StringIO) as mock_stdout:
        cli.do_play("")
        output = mock_stdout.getvalue()

    mock_game.run.assert_called_once()
    assert "TestWinner wins with 100 points!" in output


def test_do_change_name_without_game():
    """do_change_name should not run without active game"""
    cli = PiggyCLI()
    cli.menu.change_name = Mock()

    with patch('sys.stdout', new_callable=io.StringIO) as mock_stdout:
        cli.do_change_name("")
        output = mock_stdout.getvalue()

    assert "No game yet. Start one with: new" in output
    cli.menu.change_name.assert_not_called()


def test_do_change_name_with_game():
    """do_change_name should call menu change_name method"""
    cli = PiggyCLI()
    cli.game = Mock()
    cli.menu.change_name = Mock(return_value="Name changed")

    with patch('sys.stdout', new_callable=io.StringIO) as mock_stdout:
        cli.do_change_name("")
        output = mock_stdout.getvalue()

    assert "Name changed" in output
    cli.menu.change_name.assert_called_once()


def test_do_highscore_command():
    """do_highscore should display high scores"""
    cli = PiggyCLI()
    mock_highscore = Mock()
    mock_highscore.show = Mock()

    with patch('src.cli.HighScore', return_value=mock_highscore), \
            patch('sys.stdout', new_callable=io.StringIO) as mock_stdout:
        cli.do_highscore("")
        output = mock_stdout.getvalue()

    assert "High Score:" in output
    mock_highscore.show.assert_called_once()


def test_do_score_without_game():
    """do_score should not run without active game"""
    cli = PiggyCLI()

    with patch('sys.stdout', new_callable=io.StringIO) as mock_stdout:
        cli.do_score("")
        output = mock_stdout.getvalue()

    assert "No game yet. Start one with: new" in output


def test_do_score_with_game():
    """do_score should display scoreboard"""
    cli = PiggyCLI()
    mock_game = Mock()
    cli.game = mock_game

    with patch('src.cli.scoreboard_header') as mock_header, \
            patch('sys.stdout', new_callable=io.StringIO):
        cli.do_score("")

    mock_header.assert_called_once_with(mock_game)


def test_do_quit_command():
    """do_quit should return True to exit cmd loop"""
    cli = PiggyCLI()

    result = cli.do_quit("")

    assert result is True


def test_do_input_command():
    """do_input should return input result"""
    cli = PiggyCLI()

    with patch('builtins.input', return_value="test_input"):
        result = cli.do_input("Enter something: ")

    assert result == "test_input"


def test_cli_inherits_from_cmd():
    """PiggyCLI should be a subclass of cmd.Cmd"""
    cli = PiggyCLI()

    assert isinstance(cli, cmd.Cmd)


def test_multiple_cli_instances_independent():
    """Multiple CLI instances should have independent states"""
    cli1 = PiggyCLI()
    cli2 = PiggyCLI()

    cli1.game = Mock()

    assert cli1.game is not None
    assert cli2.game is None
    assert cli1 is not cli2