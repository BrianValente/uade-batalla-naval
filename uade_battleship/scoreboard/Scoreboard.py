import json
from typing import TypedDict
from uade_battleship.utils import FileStorage


class Score(TypedDict):
    name: str
    score: int


class Scoreboard:
    SCOREBOARD_FILE = "scoreboard.json"

    @staticmethod
    def get_scoreboard():
        data = FileStorage.read_file(Scoreboard.SCOREBOARD_FILE)
        if data is None:
            return []

        json_data = json.loads(data)
        scores = []
        for score in json_data:
            scores.append(Score(name=score["name"], score=score["score"]))
        return scores

    @staticmethod
    def save_score(score: Score):
        scores = Scoreboard.get_scoreboard()

        # If the score exists (same name and score), don't save it
        for s in scores:
            if s["name"] == score["name"] and s["score"] == score["score"]:
                return

        scores.append(score)
        scores.sort(key=lambda x: x["score"], reverse=True)

        json_data = json.dumps(scores)
        FileStorage.write_file(Scoreboard.SCOREBOARD_FILE, json_data)
