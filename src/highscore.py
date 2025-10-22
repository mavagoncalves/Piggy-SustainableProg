import json
import os
import time

class HighScore:
    """HighScore ranked by margin: (score - opp_score), then by score, then by earlier timestamp."""
    def __init__(self):
        base_dir = os.path.dirname(os.path.dirname(__file__))
        data_dir = os.path.join(base_dir, "data")
        os.makedirs(data_dir, exist_ok=True)
        self.file = os.path.join(data_dir, "highscore.json")
        self.limit = 10

    def load(self):
        '''Loads highscore data from file'''
        if not os.path.exists(self.file):
            return []
        try:
            with open(self.file, "r", encoding="utf-8") as f:
                data = json.load(f)
        except Exception:
            return []
        cleaned = []
        for e in data if isinstance(data, list) else []:
            name = str(e.get("name", "Player"))[:20]
            score = int(e.get("score", 0))
            opp_name = str(e.get("opponent", "Opponent"))[:20]
            opp_score = int(e.get("opp_score", 0))
            margin = int(e.get("margin", score - opp_score))
            ts = int(e.get("ts", time.time()))
            cleaned.append({
                "name": name, "score": score,
                "opponent": opp_name, "opp_score": opp_score,
                "margin": margin, "ts": ts
            })
        return cleaned

    def save(self, scores):
        '''Saves highscore data to file'''
        with open(self.file, "w", encoding="utf-8") as f:
            json.dump(scores, f, ensure_ascii=False, indent=2)

    # NEW: add_result with opponent + margin
    def add_result(self, winner_name, winner_score, opponent_name, opponent_score):
        '''Adds a new highscore entry'''
        if not winner_name:
            return
        scores = self.load()
        entry = {
            "name": winner_name.strip()[:20],
            "score": int(winner_score),
            "opponent": (opponent_name or "Opponent").strip()[:20],
            "opp_score": int(opponent_score),
            "margin": int(winner_score) - int(opponent_score),
            "ts": int(time.time()),
        }
        scores.append(entry)
        scores.sort(key=lambda e: (-e["margin"], -e["score"], e["ts"]))
        self.save(scores[: self.limit])

    # Back-compat (optional): if old calls exist
    def add(self, name, score, opponent_score=0):
        '''Back-compat: Adds a new highscore entry without opponent'''
        self.add_result(name, int(score), "—", int(opponent_score))

    def show(self):
        '''Displays the highscore list'''
        scores = self.load()
        if not scores:
            print("\nNo highscores yet.\n"); return
        scores.sort(key=lambda e: (-e["margin"], -e["score"], e["ts"]))
        print("\n--- TOP 10 (by margin) ---")
        for i, s in enumerate(scores[: self.limit], start=1):
            print(f"{i:2}. {s['name']:<20} +{s['margin']:>3}  vs {s['opponent']:<12} ({s['score']}-{s['opp_score']})")
        print("---------------------------")



