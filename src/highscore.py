import json
import os

class HighScore:
    def __init__(self, file_path=os.path.join("data", "highscore.json")):
        self.file = file_path
    
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
        scores = self._load()
        scores.append({"name": name, "score": int(score)})
        scores = sorted(scores, key=lambda x: x["score"], reverse=True)[:3]
        self._save(scores)
    
    def top(self):
        return self._load()

