import cmd
from src.menu import Menu
from src.game import Game

def scoreboard_header(game: Game):
    """Header callback injected into Game.ui_header(game)."""
    p1 = getattr(game, "player1", None)
    p2 = getattr(game, "player2", None)
    print("\n===== SCOREBOARD =====")
    if p1:
        print(f"{getattr(p1, 'name', 'P1')}: {getattr(p1, 'score', 0)}")
    if p2:
        print(f"{getattr(p2, 'name', 'P2')}: {getattr(p2, 'score', 0)}")
    current = getattr(game, "current_player", None)
    if current:
        print(f"Turn: {getattr(current, 'name', '?')}")
    print("======================\n")

class PiggyCLI(cmd.Cmd):
    intro = "Welcome to Piggy! Type 'menu' to see commands."
    prompt = "piggy> "

    def __init__(self):
        super().__init__()
        self.menu = Menu(cli=self)  # Pass self to Menu
        self.game: Game | None = None

    def _bind_game(self, g: Game):
        self.game = g
        self.menu.game = g
        setattr(self.game, "ui_header", scoreboard_header)

    def _need_game(self) -> bool:
        if self.game is None:
            print("No game yet. Start one with: new")
            return False
        return True

    def do_menu(self, arg):
        """Show the main menu options."""
        print(self.menu.display())

    def do_rules(self, arg):
        """Show rules."""
        print(self.menu.rules())

    def do_new(self, arg):
        """Create a new game."""
        print("Loading Game...")
        g = Game()
        if not getattr(g, "game_on", True):
            print("Game not started.")
            return
        self._bind_game(g)
        scoreboard_header(self.game)

    def do_play(self, arg):
        """Run the game loop."""
        if not self._need_game():
            return
        self.game.run()
        if getattr(self.game, "winner", None):
            print(f"\n{self.game.winner.name} wins with {self.game.winner.score} points!")
            scoreboard_header(self.game)

    def do_change_name(self, arg):
        """Change player names."""
        if not self._need_game():
            return
        print(self.menu.change_name())

    def do_highscore(self, arg):
        """Show highscores."""
        from src.highscore import HighScore
        print("High Score:")
        HighScore().show()

    def do_score(self, arg):
        """Show the scoreboard."""
        if not self._need_game():
            return
        scoreboard_header(self.game)

    def do_quit(self, arg):
        """Quit."""
        return True

    def do_input(self, arg):
        """Helper command to prompt for input."""
        return input(arg)

    def emptyline(self):
        pass
