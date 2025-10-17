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
                #Connect to rules here when ready
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





