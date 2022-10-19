

class Difficulty:
    def __init__(self, name="Medium", points_multiplier=2):
        if type(name) != str or type(points_multiplier) != int:
            raise ValueError
        self.name = name
        self.points_multiplier = points_multiplier

    def __repr__(self):
        return f"Difficulty {self.name} with {self.points_multiplier}x point multiplier"