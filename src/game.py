from dice import Dice
from player import Player
from ai import AI


class Game:
    def __init__(self):
        self.player1 = Player(input('Enter name for Player 1: '))
        self.dice=Dice(6)
        self.current_player=None #ASIGNAR A JUGADOR UNO DENTR ODE LAS OPCIONES SIGUIENTES, POR SI SE ESCOGE EXIT
        self.winner=None
        self.vs_ai=False
        self.ai_controller=None
        self.round_score=0
        self.game_on=True   #GAME RUNNING

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


    def run(self):  #Main function to run the whole thing

        if not self.game_on:
            return
        while self.game_on and not self.winner: #Checking the game is on and there is NO winner
            self.plays_turn()   #Plays whole turn

            if not self.winner:
                self.change_player()


    def plays_turn(self):
        if not self.game_on:    #checking the game is running
            return

        self.round_score=0 #RESTARTS THE ROUND SCORE WITH EACH START
        print(f"\nIt is {self.current_player.name}'s turn.")
        print(f"{self.current_player.name} has {self.current_player.score} points.\n") #POINTS REMINDER

        if self.vs_ai and self.current_player ==self.player2:   #Checking it is the ai turn, it runs the function
            self.ai_turn()
            return


        #TURN STARTS
        while True:
            choice=input("Press 'r' to roll or 'q' to quit").strip().lower()

            if choice=="q":
                print("Game ended without winner!")
                self.game_on=False  #Closes the game before quitting
                return
            #   CHEAT MENU ACCESS (OPTION HIDDEN)
            elif choice=="cheats":
                self.cheat_menu()
                continue

            #   GAME CONTINUES
            roll=self.dice.roll() # ROLLS THE DICE AND GETS A VALUE, STORED IN VARIABLE
            print(f"{self.current_player.name} rolled a {self.dice.face()} -> {roll}") #   PRINTS THE VALUE + ICON

            if roll!=1: #CONTINUES
                self.round_score += roll
                print(f"Current round points: {self.round_score}")
                choice=input("Roll again or hold? (r/h)").strip().lower()

                if choice in ["hold","h"]:
                    self.current_player.add_score(self.round_score)
                    if self.check_score():  #CHECKS SCORE TO END GAME
                        return
                    break
                elif choice not in ["roll", "r"]:
                    print("Invalid choice, please write 'r', 'roll', 'h' or 'hold'")

            else: #LOOSES TURN
                print(f"{self.current_player.name} lost the score and the turn!")
                self.change_player()  # CHANGES PLAYER FOR NEXT TURN
                break


    def ai_turn(self):  #AI'S TURN
        print(f"{self.current_player.name} is playing")
        self.round_score=0

        while True:
            opponent=self.player1 if self.current_player==self.player2 else self.player2
            decision=self.ai_controller.decide_difficulty(self.current_player.score, opponent.score,self.round_score)
            roll=self.dice.roll()
            print(f"{self.current_player.name} rolled a {self.dice.face()} -> {roll}")

            if roll==1: #LOOSES TURN
                print(f"{self.current_player.name} lost the score and the turn!")
                return
            self.round_score += roll
            print(f"AI round points: {self.round_score} (decision:{decision})")

            if decision=="hold":
                self.current_player.add_score(self.round_score)
                if self.check_score():
                    return
                break


    def change_player(self):

        if self.current_player==self.player1:
            self.current_player=self.player2
        else:
            self.current_player=self.player1


    def check_score(self):

        if self.current_player.score>=100:
            self.winner=self.current_player
            print(f"{self.current_player.name} wins with {self.current_player.score} points.!")
            return True
        return False

    def cheat_menu(self):

        while True:
            if self.current_player.score>=100:  #Checks of the player tries to get in again after being kicked out
                print('Maximum score reached! Cheat menu will close now\n')
                break
            self.show_cheat_menu()
            choice_cheats = input("Choose option: ")

            if choice_cheats=="1":  # OPTION 1 - ADDING POINTS
                try:
                    score_cheat=int(input("Enter score to add: "))
                except ValueError:
                    print("Invalid choice, enter a number.")
                    continue

                if not (1<=score_cheat<=100):
                    print("Invalid choice, enter value between 1-100")
                    continue
                self.current_player.add_score(score_cheat)
                setattr(self.current_player, "cheat_use", True) #ATTRIBUTE CREATED FOR PLAYER FOR CHEATS USED

            elif choice_cheats=="2":    # OPTION 2 - SUBTRACTING POINTS
                try:
                    score_cheat=int(input("Enter score to subtract: "))
                except ValueError:
                    print("Invalid choice, enter a number.")
                    continue
                hypothetical_score = self.current_player.score - score_cheat

                if not (1<=score_cheat<=100):
                    print("Invalid choice, enter value between 1-100")
                    continue
                if hypothetical_score<0:
                    print("Invalid choice, your score can't be less than 0")
                    continue
                self.current_player.score-=score_cheat
                setattr(self.current_player, "cheat_use", True) #ATTRIBUTE CREATED FOR CHEATS USED

            elif choice_cheats=="3":    # QUIT - JUST QUITTING lol
                break
            else:
                print("Invalid option: please select '1', '2' or '3'.")


    def show_cheat_menu(self):
        print(f"""WELCOME TO CHEAT MENU
            - press 1 to add points
            - press 2 to subtract points
            - press 3 to quit the cheat  menu
            Current points: {self.current_player.score}""")