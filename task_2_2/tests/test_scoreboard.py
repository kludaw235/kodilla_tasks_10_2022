import pytest
import os
import sys
from task_2_2.scoreboard import Scoreboard
from task_2_2.modules.quiz import Quiz
from task_2_2.modules.users import Users


@pytest.fixture(autouse=True)
def no_json_dump(monkeypatch):
    monkeypatch.delattr('json.dump')


@pytest.fixture()
def scoreboard():
    return Scoreboard(".\\tests\\test_sorted.json")


def test_json_file_exists(scoreboard):
    scoreboard_path_full = sys.modules[scoreboard.__module__].__file__
    scoreboard_path_folder = os.path.dirname(scoreboard_path_full)
    assert os.path.exists(scoreboard_path_folder + "\\myfile.json")


@pytest.fixture()
def scores():
    return {"users": [{
        "name": "John",
        "score": 200,
        "rank": 5,
    }]}


def test_get_scoreboard_data_return(scoreboard):
    sb = scoreboard.get_scoreboard()
    assert sb["users"][2]["name"] == "izo"
    assert sb["users"][2]["score"] == 1
    assert sb["users"][2]["rank"] == 3


@pytest.mark.parametrize('score, expected', (
        (2, 3),
        (0, 4),
        (1, 3),
        (199, 2),
        (1000, 1),
))
def test_user_rank_valid_score(scoreboard, score, expected):
    assert scoreboard.get_user_rank(score) == expected


def test_user_rank_invalid_score(scoreboard):
    assert scoreboard.get_user_rank(-100) == 4


def test_setting_rank_by_index(scoreboard, scores):
    json_rank = scoreboard.set_users_ranks_by_index(scores)
    assert json_rank["users"][0]["rank"] == 1


@pytest.fixture()
def user():
    return Users(
        id=1,
        name="John",
        email="john@scoreboard.com",
        password="super_secret",
        is_active=True,
        is_admin=True,
        quizzes=[],
    )


@pytest.mark.parametrize('difficulty, expected', (
        ("Easy", 1),
        ("Medium", 2),
        ("Hard", 3),
        ("Very hard", 4)
))
def test_user_score_multiplier(scoreboard, user, difficulty, expected):
    quiz = Quiz(user_id=1, correct_answers=1, difficulty=difficulty)
    user.quizzes = [quiz]
    user_score = scoreboard.get_user_score(user)
    assert user_score == expected


@pytest.mark.parametrize('correct_answer, expected', (
        (0, 0),
        (4, 8),
        (7, 14),
        (10, 20)
))
def test_user_score_correct_answers(scoreboard, user, correct_answer, expected):
    quiz = Quiz(user_id=1, correct_answers=correct_answer, difficulty="Medium")
    user.quizzes = [quiz]
    user_score = scoreboard.get_user_score(user)
    assert user_score == expected


@pytest.mark.parametrize('difficulty, correct_answer, expected', (
        ("", 1, 0),
        ("ABC", 1, 0),
        ("Medium", -1, 0),
        ("Medium", 11, 0)
))
def test_user_score_invalid_data(scoreboard, user, difficulty, correct_answer, expected):
    quiz = Quiz(user_id=1, correct_answers=correct_answer, difficulty=difficulty)
    user.quizzes = [quiz]
    user_score = scoreboard.get_user_score(user)
    assert user_score == expected


# Integrity tests

@pytest.fixture
def scoreboard_integrity():
    scoreboard = Scoreboard(data_file="test_sorted.json")
    scoreboard.init_scoreboard()
    return scoreboard

# def test_get_user_score(scoreboard, user):
#     mocker.patch('db.get_all_games', return_value=[Quiz(), Quiz(), Quiz()])
#     score = scoreboard.get_user_score(user)
#     assert score == 2
