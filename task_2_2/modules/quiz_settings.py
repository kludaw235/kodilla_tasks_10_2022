from .difficulty import Difficulty

LEVEL_MULTIPLIER = {
            "Easy": 1,
            "Medium": 2,
            "Hard": 3,
            "Very hard": 4
}

class QuizSettings:
    def __init__(self):
        self.difficulties = []
        for key, value in LEVEL_MULTIPLIER.items():
            self.difficulties.append(Difficulty(name=key, points_multiplier=value))

        self.categories = ["Movie", "Music", "Economy", "Animals"]