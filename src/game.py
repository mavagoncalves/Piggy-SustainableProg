from dice import Dice
from player import Player


class Game:
    def __init__(self):
        self.round_score = 0
        self.dice=Dice(6)
        self.player1=Player(input('Enter name for player 1: ')) #AQUI EL NOMBRE
        self.player2=Player(input('Enter name for player 2: ')) #AQUI EL OTRO NOMBRE
        self.current_player=self.player1 #FIRST TURN ASSIGNED ALWAYS TO PLAYER 1, THEN CHANGES
        self.winner=None    #DEFINED FOR THE SCORE THINGY

    def plays_turn(self):
        self.round_score=0 #RESTARTS THE ROUND SCORE WITH EACH START
        print(f"\nIt is {self.current_player.name}'s turn.")
        print(f"{self.current_player.name} has {self.current_player.score} points.\n") #POINTS REMINDER

        #TURN STARTS
        while True:
            choice=input("Press 'r' to roll or 'q' to quit").strip().lower()
            if choice=="q":
                print("Game ended without winner!")
                return
            #   CHEAT MENU ACCESS (OPTION HIDDEN)
            elif choice=="cheats":
                self.cheat_menu()

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
                print(f"{self.current_player.name} lost the score adn the turn!")
                self.change_player()  # CHANGES PLAYER FOR NEXT TURN
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
        else:
            return False

    def cheat_menu(self):
        while True:
            if self.current_player.score>=100:
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
                setattr(self.current_player, "cheat_use", True) #ATTRIBUTE CREATED FOR CHEATS USED
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