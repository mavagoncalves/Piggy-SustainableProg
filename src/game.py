from dice import Dice
from player import Player


class Game:
    def __init__(self):
        self.round_score = 0
        self.dice=Dice(6)
        self.player1=Player("NOMBRE1") #AQUI EL NOMBRE
        self.player2=Player("NOMBRE2") #AQUI EL OTRO NOMBRE
        self.current_player=self.player1 #FIRST TURN ASSIGNED ALWAYS TO PLAYER 1, THEN CHANGES
        self.winner=None    #DEFINED FOR THE SCORE THINGY

    def plays_turn(self):
        self.round_score=0 #RESTARTS THE ROUND SCORE WITH EACH START
        print(f"\nIt is {self.current_player}'s turn.")
        print(f"{self.current_player} has {self.current_player.score} points.\n") #POINTS REMINDER

        #TURN STARTS
        while True:
            choice=input("Press ENTER to roll or 'q' to quit").strip().lower()
            # OPTION TO END GAME HERE
            if choice=="q":
                print("Game ended without winner!")
                exit()

            # GAME CONTINUES
            roll=self.dice.roll() #ROLLS THE DICE AND GETS A VALUE, STORED IN VARIABLE
            print(f"{self.current_player} rolled a {self.dice.turn()}") #PRINTS THE VALUE + ICON
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
                print(f"{self.current_player} lost the score!")
                self.change_player()  #CHANGES PLAYER FOR NEXT TURN
                break


    def change_player(self):
        if self.current_player==self.player1:
            self.current_player=self.player2
        else:
            self.current_player=self.player1

    def check_score(self):
        if self.current_player.score>=100:
            self.winner=self.current_player
            print(f"{self.current_player} wins with {self.current_player.score} points.!")
            return True
        else:
            return False




    # FUNCION PARA LOS TRUCOS

    def cheat_menu(self):
        print(f"""WELCOME TO CHEAT MENU
-   press 1 to add 5 points
-   press 2 to add 20 points
-   press 3 to add 50 points
-   press 4 to quit the cheat  menu
Current points: {self.current_player.score}""")
        choice_cheats=input("Choose option: ")
        if choice_cheats=="1":  # OPTION 1
            hypothetical_result=self.current_player.score+5
            if  hypothetical_result>=100:
                print("If you do this action you will reach the score goal and finish the game in the next round.")
                choice_menu=input("Are you sure? (y/n)").lower()
                if choice_menu=="y":
                    self.current_player.score += 5
                    cheats_used=True
            else:
                self.current_player.score += 5
        elif choice_cheats=="2":    # OPTION 2
            hypothetical_result=self.current_player.score+20
            if  hypothetical_result>=100:
                print("If you do this action you will reach the score goal and finish the game in the next round.")
                choice_menu=input("Are you sure? (y/n)").lower()
                if choice_menu=="y":
                    self.current_player.score += 20
                    cheats_used = True
            else:
                self.current_player.score += 20
        elif choice_cheats=="3":  # OPTION 3
            hypothetical_result = self.current_player.score + 50
            if hypothetical_result >= 100:
                print("If you do this action you will reach the score goal and finish the game in the next round.")
                choice_menu = input("Are you sure? (y/n)").lower()
                if choice_menu == "y":
                    self.current_player.score += 50
                    cheats_used = True
            else:
                self.current_player.score += 50