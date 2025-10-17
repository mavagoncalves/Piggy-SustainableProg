import json
import os

class HighScore:
    def __init__(self, file_path=os.path.join("data", "highscore.json")):
        self.file = file_path
