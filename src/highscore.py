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

