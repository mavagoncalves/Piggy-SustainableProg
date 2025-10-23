'''Main Game class for Piggy game'''
from src.dice import Dice
from src.player import Player
from src.ai import AI
from src.cheat import Cheat
from src.highscore import HighScore


class Game: # pylint: disable=too-many-instance-attributes
    '''Main Game class to control the game flow
    Attributes:
    - player1: Player object for player 1
    - player2: Player object for player 2 or AI
    - dice: Dice object to roll the dice
    - current_player: Player object for the current player
    - winner: Player object for the winner
    - vs_ai: Boolean to check if playing against AI
    - ai_controller: AI object to control the AI player
    - round_score: Integer to keep track of the current round score
    - game_on: Boolean to check if the game is running
    - cheats: Cheat object to handle cheat codes
    '''
    def __init__(self):
        self.player1 = Player(input('Enter name for Player 1: '))
        self.dice=Dice()
        self.current_player=None
        self.winner=None
        self.vs_ai=False
        self.ai_controller=None
        self.round_score=0
        self.game_on=True   #GAME RUNNING
        self.cheats=Cheat(self) #Cheat class call
        self.scoreboard_header=None  #Placeholder for scoreboard header callback

        mode=input("----------GAME MODES----------" \
        "\n1) PvP \n2) PvAI \n3) Exit \nYour choice: ").strip()
        if mode=="1":
            self.player2 = Player(input('Enter name for Player 2: '))
            self.current_player = self.player1

        elif mode=="2":
            difficulty=input("Select AI difficulty (easy/medium/hard): ").strip().lower()

            if difficulty not in ["easy","medium","hard"]:
                print("Invalid difficulty, exiting...")
                self.game_on=False  #EXITING HERE
                return
            self.player2 = Player("AI")
            self.ai_controller = AI(difficulty)
            self.vs_ai=True
            self.current_player = self.player1

        elif mode=="3":
            print("Exiting...")
            self.game_on=False  #EXITING HERE
            return

        else:
            print("Invalid option, exiting...")
            self.game_on=False   #EXITING HERE
            return


    def run(self):
        """Runs the game loop until there is a winner or the game is ended"""
        if not self.game_on:
            return

        while self.game_on and not self.winner:
            if hasattr(self, "ui_header") and callable(self.ui_header):
                self.ui_header(self)

            self.plays_turn()  # play exactly one turn for current_player

            if self.game_on and not self.winner:
                self.change_player()


    def plays_turn(self):
        """Plays a single turn for the current player"""
        if not self.game_on:
            return

        self.round_score = 0

        print(f"\nIt is {self.current_player.name}'s turn.")
        print(f"{self.current_player.name} has {self.current_player.score} points.\n")

        # run() does the flip.
        if self.vs_ai and self.current_player == self.player2:
            self.ai_turn()
            return

        while True:
            if self.round_score > 0:
                print(f"Current round points: {self.round_score}")

            choice = input("Choose: roll (r), hold (h), or quit (q): ").strip().lower()

            if choice == "hidden":
                self.cheats.cheat_menu()
                continue

            if choice in ("q", "quit"):
                print("Game ended without winner!")
                self.game_on = False
                return

            if choice in ("h", "hold"):
                if self.round_score == 0:
                    print("You can't hold 0 points. Roll first.")
                    continue
                self.current_player.add_score(self.round_score)
                if self.check_score():  # may set winner and stop the game loop
                    return
                return

            if choice in ("r", "roll"):
                roll = self.dice.roll()
                print(f"{self.current_player.name} rolled a {self.dice.face()} -> {roll}")

                if roll == 1:
                    print(f"{self.current_player.name} rolled a 1 and loses the turn!")
                    return

                self.round_score += roll
                continue

            print("Invalid choice. Please enter 'r' to roll, 'h' to hold, or 'q' to quit.")

    def ai_turn(self):
        """Plays a turn for the AI player"""
        print(f"{self.current_player.name} is playing")
        self.round_score = 0

        while True:
            opponent = self.player1 if self.current_player == self.player2 else self.player2
            decision = self.ai_controller.decide_difficulty(
                self.current_player.score, opponent.score, self.round_score
            )
            roll = self.dice.roll()
            print(f"{self.current_player.name} rolled a {self.dice.face()} -> {roll}")

            if roll == 1:
                print(f"{self.current_player.name} lost the score and the turn!")
                return  # run() will change player

            self.round_score += roll
            print(f"AI round points: {self.round_score} (decision: {decision})")

            if decision == "hold":
                self.current_player.add_score(self.round_score)
                if self.check_score():
                    return
                return

    def change_player(self):
        '''Switches the current player'''
        if self.current_player==self.player1:
            self.current_player=self.player2
        else:
            self.current_player=self.player1

    def check_score(self):
        """Check if current player won, announce result, and save human wins only."""
        if self.current_player.score >= 100:
            print(f"\n{self.current_player.name} wins with {self.current_player.score} points!\n")

            # Figure out opponent
            opponent = self.player2 if self.current_player is self.player1 else self.player1

            # If AI wins, don't save to highscores
            ai_won = (
                isinstance(self.current_player, AI)
                or getattr(self.current_player, "is_ai", False)
                or str(self.current_player.name).strip().lower() in {"ai", "computer", "cpu"}
            )
            if ai_won:
                self.game_on = False
                return True

            # Human winner -> save result ranked by margin
            hs = HighScore()
            hs.add_result(
                winner_name=self.current_player.name,
                winner_score=self.current_player.score,
                opponent_name=opponent.name,
                opponent_score=opponent.score,
            )
            self.game_on = False
            return True

        return False
