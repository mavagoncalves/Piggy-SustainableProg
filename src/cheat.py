class Cheat:
    def __init__(self,game):
        self.game=game
        self.current = None #Renaming for shorter name

    def cheat_menu(self):
        while True:
            self.current=self.game.current_player   #Local access
            if self.current.score >= 100:  # Checks of the player tries to get in again after being kicked out
                print('Maximum score reached! Cheat menu will close now\n')
                break
            self.show_cheat_menu()
            choice_cheats = input("Choose option: ").strip()

            if choice_cheats == "1":  # OPTION 1 - ADDING POINTS
                try:
                    score_cheat = int(input("Enter score to add: "))
                except ValueError:
                    print("Invalid choice, enter a number.")
                    continue

                if not (1 <= score_cheat <= 100):
                    print("Invalid choice, enter value between 1-100")
                    continue
                self.current.add_score(score_cheat)
                setattr(self.current, "cheat_use", True)  # ATTRIBUTE CREATED FOR PLAYER FOR CHEATS USED

            elif choice_cheats == "2":  # OPTION 2 - SUBTRACTING POINTS
                try:
                    score_cheat = int(input("Enter score to subtract: "))
                except ValueError:
                    print("Invalid choice, enter a number.")
                    continue
                hypothetical_score = self.current.score - score_cheat

                if not (1 <= score_cheat <= 100):
                    print("Invalid choice, enter value between 1-100")
                    continue
                if hypothetical_score < 0:
                    print("Invalid choice, your score can't be less than 0")
                    continue
                self.current.score -= score_cheat
                setattr(self.current, "cheat_use", True)  # ATTRIBUTE CREATED FOR CHEATS USED

            elif choice_cheats == "3":  # QUIT - JUST QUITTING lol
                break
            else:
                print("Invalid option: please select '1', '2' or '3'.")


    def show_cheat_menu(self):
        print(f"""WELCOME TO CHEAT MENU
            - press 1 to add points
            - press 2 to subtract points
            - press 3 to quit the cheat  menu
            Current points: {self.current.score}""")    #Value already assigned for 'current' before this function is called