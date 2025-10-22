from src.cli import PiggyCLI

def main():
    """Entry point for the Piggy game."""
    cli = PiggyCLI()
    cli.cmdloop()

if __name__ == "__main__":
    main()
