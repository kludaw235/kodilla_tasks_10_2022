from .difficulty import Difficulty

class QuizSettings:
    def __init__(self):
        self.difficulties = []
        self.categories = []

    def load_difficulties(self):
        self.difficulties.append(Difficulty(name="Easy", points_multiplier=1))
        self.difficulties.append(Difficulty(name="Medium", points_multiplier=2))
        self.difficulties.append(Difficulty(name="Hard", points_multiplier=3))
        self.difficulties.append(Difficulty(name="Very hard", points_multiplier=4))

    def load_categories(self):
        self.categories.append("Movie")
        self.categories.append("Music")
        self.categories.append("Economy")
        self.categories.append("Animals")
