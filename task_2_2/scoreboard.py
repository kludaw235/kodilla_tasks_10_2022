import os
import json
from task_2_2.querries import DatabaseQuerries

db = DatabaseQuerries()

LEVEL_MULTIPLIER = {
            "Easy": 1,
            "Medium": 2,
            "Hard": 3,
            "Very hard": 4
}

class Scoreboard():
    def __init__(self, data_file):
        self.__json_path = os.path.dirname(__file__) + "/" + data_file

    def init_scoreboard(self):
        if not os.path.exists(self.__json_path):
            with open(self.__json_path, "w", encoding="utf-8") as json_file:
                json.dumps({"users": []}, json_file, indent=4)


    def get_scoreboard(self):
        with open(self.__json_path, "r", encoding="utf-8") as json_file:
            json_data = json.load(json_file)
        return json_data

    def get_user_rank(self, score):
        scoreboard = self.get_scoreboard()
        rank = len(scoreboard["users"]) + 1
        for scoreboard_user in scoreboard["users"]:
            if score >= scoreboard_user["score"]:
                rank = scoreboard_user["rank"]
                break
        return rank

    def set_users_ranks_by_index(self, json_score_sorted):
        for sorted_user in json_score_sorted["users"]:
            index = json_score_sorted["users"].index(sorted_user)
            sorted_user["rank"] = index + 1
        return json_score_sorted

    def update_score(self, user):
        score = self.get_user_score(user)
        with open(self.__json_path, "r+", encoding="utf-8") as json_file:
            json_temp = json.load(json_file)
            unique = True
            for json_user in json_temp["users"]:
                if json_user['name'] == user.name:
                    json_user['score'] = score
                    json_user['rank'] = self.get_user_rank(score)
                    unique = False
            if unique:
                json_temp["users"].append({"name": user.name, "score": score, "rank": None})
            json_file.seek(0)
            json_temp["users"].sort(key=lambda x: x["score"], reverse=True)
            json_temp = self.set_users_ranks_by_index(json_temp)
            json.dump(json_temp, json_file, indent=4)

    def get_user_score(self, user):
        score = 0
        all_games = db.get_all_games(user)
        for game in all_games:
            try:
                multiplier = LEVEL_MULTIPLIER[game.difficulty]
            except KeyError:
                multiplier = 0
            if game.correct_answers < 0 or game.correct_answers > 10:
                multiplier = 0
            score += (game.correct_answers * multiplier)
        return score
