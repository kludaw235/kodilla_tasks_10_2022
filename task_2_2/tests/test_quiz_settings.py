from task_2_2.modules.quiz_settings import QuizSettings
from task_2_2.modules.difficulty import Difficulty
import pytest

@pytest.fixture()
def quiz_settings():
    return QuizSettings()

def test_proper_categories(quiz_settings):
    assert quiz_settings.categories == ["Movie", "Music", "Economy", "Animals"]

def test_proper_difficulties(quiz_settings):
    assert str(quiz_settings.difficulties) == str([Difficulty("Easy", 1),
                                          Difficulty("Medium", 2),
                                          Difficulty("Hard", 3),
                                          Difficulty("Very hard", 4)])
