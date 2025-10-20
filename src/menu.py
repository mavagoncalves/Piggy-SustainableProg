from src.game import Game
from src.highscore import HighScore


class Menu:
    def __init__(self):
        self.game = None
        self.running = True

    def display(self):
        print("=== MAIN MENU ===")
        print("1. Rules")
        print("2. New Game")
        print("3. Change Name")
        print("4. High Score")
        print("5. Quit")

    def run(self):
        while self.running:
            self.display()
            choice = input("Enter your choice: ")

            if choice == "1":
                rules(self)
            elif choice == "2":
                print("Loading Game...")
                self.game = Game()
                self.game.run()
            elif choice == "3":
                change_name(self)
            elif choice == "4":
                print("High Score:")
                highscore = HighScore()
                highscore.show()
            elif choice == "5":
                print("Quitting...")
                self.running = False
            else:
                print("Invalid choice. Please enter a number between 1 and 5.")

    def rules(self):
        print("Rules:")
        print("1. Players: 2 players take turns.")
        print("2. Goal: Be the first to reach 100 points.")
        print("3. On your turn:")
        print("- Roll a single 6-sided die as many times as you want.")
        print("- Each roll adds its value to your turn total.")
        print("4. If you roll a 1:")
        print("- Your turn ends immediately.")
        print("- You lose all points earned in that turn.")
        print("- Your overall score stays the same.")
        print("5. If you “Hold”:")
        print("- Add your turn total to your overall score.")
        print("- Pass the die to the next player.")
        print("6. Winning:")
        print("- The first player to reach 100 or more points wins the game.")

    def change_name(self):
        if not self.game:
            print("No game in progress.")
            return
        print("Change Name:")
        new_name1 = input(f"Enter new name for Player 1 ({self.game.player1.name}): ").strip()
        if new_name1:
            self.game.player1.change_name(new_name1)
            print(f"Name of player 1 changed to {self.game.player1.name}")
        new_name2 = input(f"Enter new name for Player 2 ({self.game.player2.name}): ").strip()
        if new_name2:
            self.game.player2.change_name(new_name2)
            print(f"Name of player 2 changed to {self.game.player2.name}")






if __name__ == "__main__":
    menu = Menu()
    menu.run()


