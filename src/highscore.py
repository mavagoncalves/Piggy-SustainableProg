import json
import os

class HighScore:
    def __init__(self):
        base_dir = os.path.dirname(os.path.dirname(__file__))
        data_dir = os.path.join(base_dir, "data")
        os.makedirs(data_dir, exist_ok=True)
        self.file = os.path.join(data_dir, "highscore.json")
    
    def load(self):
        if not os.path.exists(self.file):
            return []
        with open(self.file, "r") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return []

    def save(self, scores):
        with open(self.file, "w") as f:
            json.dump(scores, f, indent=2)
    
    def add(self, name, score):
        if not name:
            return
        scores = self.load()
        scores.append({"name": name, "score": int(score)})
        scores = sorted(scores, key=lambda x: x["score"], reverse=True)[:3]
        self.save(scores)
    
    def top(self):
        return self.load()
    
    def show(self):
        scores = self.load()
        if not scores:
            print("\nNo highscores yet.\n")
            return
        print("\n--- TOP 3 PLAYERS ---")
        for i, s in enumerate(scores, start=1):
            print(f"{i}. {s['name']} — {s['score']}")
        print("----------------------")

