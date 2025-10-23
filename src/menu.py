'''Menu class for PiggyCLI'''

class Menu:
    '''Menu class to support PiggyCLI commands
    Attributes:
    - game: Game object to manage the current game
    - cli: PiggyCLI object for input/output
    '''
    def __init__(self, cli=None):
        self.game = None
        self.cli = cli

    def display(self):
        '''Returns main menu options as a string'''
        return "\n".join([
            "=== MAIN MENU ===",
            "menu: Show this menu",
            "rules: Show game rules",
            "new: Start a new game",
            "change_name: Change player names",
            "highscore: View high scores",
            "score: View current scores",
            "play: Play the game",
            "quit: Exit the game"
        ])

    def rules(self):
        '''Returns game rules as a string'''
        return "\n".join([
            "Rules:",
            "1. Two players take turns rolling a 6-sided die.",
            "2. Goal: Reach 100 points first.",
            "3. Each roll adds to your turn total.",
            "4. Roll a 1: Lose turn points, turn ends.",
            "5. Hold: Add turn total to your score, pass turn.",
            "6. First to 100 points wins."
        ])

    def change_name(self):
        """Changes player names via PiggyCLI, returns result."""
        if not self.game:
            return "No game in progress."

        result = []

        name1 = self.cli.do_input(
            f"Enter new name for Player 1 ({self.game.player1.name}): "
        ).strip()
        if name1:
            self.game.player1.name = name1
            result.append(f"Player 1 name changed to {self.game.player1.name}")

        name2 = self.cli.do_input(
            f"Enter new name for Player 2 ({self.game.player2.name}): "
        ).strip()
        if name2:
            self.game.player2.name = name2
            result.append(f"Player 2 name changed to {self.game.player2.name}")

        return "\n".join(result) if result else "No names changed."
