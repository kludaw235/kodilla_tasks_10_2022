import pytest
import os
import sys
from unittest.mock import  Mock
from task_2_2.scoreboard import Scoreboard



TEST_JSON_SORTED = {"users": [
                            {   "name": "aa",
                                "score": 200,
                                "rank": 1},
                            {   "name": "bb",
                                "score": 100,
                                "rank": 2},
                            {   "name": "izo",
                                "score": 1,
                                "rank": 3}]}

TEST_JSON_UNSORTED = {"users": [
                            {   "name": "izo",
                                 "score": 1,
                                 "rank": 3},
                            {   "name": "bb",
                                "score": 100,
                                "rank": 2},
                            {   "name": "aa",
                                 "score": 200,
                                 "rank": 1}
]}

@pytest.fixture(autouse=True)
def no_json_dump(monkeypatch):
    monkeypatch.delattr('json.dump')
    monkeypatch.delattr('builtins.open')

@pytest.fixture()
def scoreboard():
    return Scoreboard()

@pytest.fixture()
def json_scoreboard(scoreboard):
    scoreboard = Scoreboard()
    scoreboard.get_scoreboard = Mock()
    scoreboard.get_scoreboard.return_value = TEST_JSON_SORTED
    return scoreboard

def test_Scoreboard_import():
    from task_2_2.scoreboard import Scoreboard
    assert callable(Scoreboard), '"Scoreboard" is not callable'

def test_json_file_exists(scoreboard):
    scoreboard_path_full = sys.modules[scoreboard.__module__].__file__
    scoreboard_path_folder = os.path.dirname(scoreboard_path_full)
    assert os.path.exists(scoreboard_path_folder + "\\myfile.json")

@pytest.mark.parametrize('score, expected', (
    (2, 3),
    (0, 4),
    (1, 3),
    (199, 2),
    (1000, 1),
))
def test_user_rank_valid_score(json_scoreboard, score, expected):
    assert json_scoreboard.get_user_rank(score) == expected

def test_user_rank_invalid_score(json_scoreboard):
    assert json_scoreboard.get_user_rank(-100) == 4

def test_sorting_json_scoreboard(scoreboard):
    json_sort = scoreboard.set_users_ranks_by_index(TEST_JSON_SORTED)
    assert json_sort == TEST_JSON_SORTED


@pytest.fixture()
def UserMock():
    UserMock = Mock()
    UserMock.quizzes = Mock()
    UserMock.quizzes.all = Mock()
    UserMock.quizzes.all.return_value = []
    return UserMock

@pytest.mark.parametrize('difficulty, expected', (
    ("Easy", 1),
    ("Medium", 2),
    ("Hard", 3),
    ("Very hard", 4)
))
def test_user_score_multiplier(scoreboard, UserMock, difficulty, expected):
    m1 = Mock()
    m1.difficulty = difficulty
    m1.correct_answers = 1
    UserMock.quizzes.all.return_value = [m1]
    x = scoreboard.get_user_score(UserMock)
    assert x == expected

@pytest.mark.parametrize('correct_answer, expected', (
    (0, 0),
    (4, 8),
    (7, 14),
    (10, 20)
))
def test_user_score_correct_answers(scoreboard, UserMock, correct_answer, expected):
    m1 = Mock()
    m1.difficulty = "Medium"
    m1.correct_answers = correct_answer
    UserMock.quizzes.all.return_value = [m1]
    x = scoreboard.get_user_score(UserMock)
    assert x == expected

@pytest.mark.parametrize('difficulty, correct_answer, expected', (
    ("", 1, 0),
    ("ABC", 1, 0),
    ("Medium", -1, 0),
    ("Medium", 11, 0)
))
def test_user_score_invalid_data(scoreboard, UserMock, difficulty, correct_answer, expected):
    m1 = Mock()
    m1.difficulty = difficulty
    m1.correct_answers = correct_answer
    UserMock.quizzes.all.return_value = [m1]
    x = scoreboard.get_user_score(UserMock)
    assert x == expected
