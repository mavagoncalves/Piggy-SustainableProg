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