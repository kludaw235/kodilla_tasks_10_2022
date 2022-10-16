

class Difficulty:
    def __init__(self, name="Medium", points_multiplier=2):
        self.name = name
        self.points_multiplier = points_multiplier

    def __repr__(self):
        return f"Difficulty {self.name} with {self.points_multiplier}x point multiplier"