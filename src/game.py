from src.dice import Dice
from src.player import Player
from src.ai import AI
from src.cheat import Cheat


class Game:
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
        self.dice=Dice(6)
        self.current_player=None
        self.winner=None
        self.vs_ai=False
        self.ai_controller=None
        self.round_score=0
        self.game_on=True   #GAME RUNNING
        self.cheats=Cheat(self) #Cheat class call

        mode=input("Choose mode:\n1) Two players \n2) Play vs AI\n3) Exit: ").strip()
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
        
        if hasattr(self, "ui_header") and callable(self.ui_header):
            self.ui_header(self)

        while self.game_on and not self.winner:
            self.plays_turn()  # play exactly one turn for current_player

            if self.game_on and not self.winner:
                self.change_player()

                if hasattr(self, "ui_header") and callable(self.ui_header):
                    self.ui_header(self)



    def plays_turn(self):
        """Plays a single turn for the current player"""
        if not self.game_on:
            return

        self.round_score = 0
        # CLI header
        if hasattr(self, "ui_header") and callable(self.ui_header):
            self.ui_header(self)

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

            if choice == "cheats":
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
        # CLI header
        if hasattr(self, "ui_header") and callable(self.ui_header):
            self.ui_header(self)

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
        '''Checks if the current player has won'''
        if self.current_player.score>=100:
            self.winner=self.current_player
            print(f"{self.current_player.name} wins with {self.current_player.score} points.!")
            return True
        return False