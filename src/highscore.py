import json
import os

FILE = os.path.join("data","highscores.json")

def load_scores():
    """Load high scores from file, return as a list of dicts."""
    if not os.path.exists(FILE):
        return []
    with open(FILE, "r") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []

def save_scores(scores):
    """Save list of score dicts to file."""
    with open(FILE, "w") as f:
        json.dump(scores, f, indent=2)