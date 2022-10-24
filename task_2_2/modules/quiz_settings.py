from .difficulty import Difficulty
from task_2_2.scoreboard import LEVEL_MULTIPLIER

class QuizSettings:
    def __init__(self):
        self.difficulties = []
        for key, value in LEVEL_MULTIPLIER.items():
            self.difficulties.append(Difficulty(name=key, points_multiplier=value))

        self.categories = ["Movie", "Music", "Economy", "Animals"]