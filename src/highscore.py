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

def add_score(name, score):
    """Add a new score and keep only the top 3."""
    if not name:
        return
    scores = load_scores()
    scores.append({"name": name, "score": score})
    # sort descending by score, keep top 3
    scores = sorted(scores, key=lambda x: x["score"], reverse=True)[:3]
    save_scores(scores)

def show_scores():
    """Print the high score table."""
    scores = load_scores()
    if not scores:
        print("\nNo highscores yet.\n")
    else:
        print("\n--- TOP 3 PLAYERS ---")
        for i, s in enumerate(scores, start=1):
            print(f"{i}. {s['name']} — {s['score']}")
        print("----------------------")