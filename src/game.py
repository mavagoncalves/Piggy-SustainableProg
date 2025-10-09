from dice import Dice
from player import Player


class Game:
    def __init__(self):
        self.round_score = 0
        self.dice=Dice(6)
        self.player1=Player("NOMBRE1") #AQUI EL NOMBRE
        self.player2=Player("NOMBRE2") #AQUI EL OTRO NOMBRE
        self.current_player=self.player1 #FIRST TURN ASSIGNED ALWAYS TO PLAYER 1, THEN CHANGES

    def plays_turn(self):
        self.round_score=0
        print(f"It is {self.current_player}'s turn.")

        #TURN STARTS
        while True:
            input("Press enter to continue or whatever")  #PREGUNTAR SI EL NUMERO ES INPUT O UN COMANDO COMO EN EL MENU
            roll=self.dice.roll() #ROLLS THE DICE AND GETS A VALUE
            print(f"{self.current_player} rolled a {self.dice.turn()}") #PRINTS THE VALUE + ICON
            if self.dice.roll()!=1:
                self.round_score += self.dice.roll()
            else:
                print(f"{self.player1} lost the score!")
                self.current_player=self.player2


    def change_player(self):
        if self.current_player==self.player1:
            self.current_player=self.player2
        else:
            self.current_player=self.player1