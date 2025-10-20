class Menu:
    def __init__(self):
        self.running = True

    def display(self):
        print("\n=== MAIN MENU ===")
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
                print("Rules:")
                rules(self)
            elif choice == "2":
                print("Loading Game...")
                #Connect to game class when ready
            elif choice == "3":
                print("Change Name:")
                #Connect to name class when ready
            elif choice == "4":
                print("High Score:")
                #Connect to high score class when ready
            elif choice == "5":
                print("Quitting...")
                self.running = False
            else:
                print("Invalid choice. Please enter a number between 1 and 5.")

def rules(self):
    print("Rules:")
    print("1. 🎲 Players: 2 players take turns.")
    print("2. 🐷 Goal: Be the first to reach 100 points.")
    print("3. 🔁 On your turn:")
    print("- Roll a single 6-sided die as many times as you want.")
    print("- Each roll adds its value to your turn total.")
    print("4. 💀 If you roll a 1:")
    print("- Your turn ends immediately.")
    print("- You lose all points earned in that turn.")
    print("- Your overall score stays the same.")
    print("5. ✋ If you “Hold”:")
    print("- Add your turn total to your overall score.")
    print("- Pass the die to the next player.")
    print("6. 🏆 Winning:")
    print("- The first player to reach 100 or more points wins the game.")








