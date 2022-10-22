import pytest
import os
import sys
import json
from unittest.mock import Mock, patch
from task_2_2.scoreboard import Scoreboard
# from pytest_mock import mocker
# from task_2_2.modules.quiz import Quiz


@pytest.fixture()
def json_sorted_content():
    test_file_path = os.path.dirname(__file__) + "\\test_sorted.json"
    with open(test_file_path, "r", encoding="utf-8") as json_file:
        json_data = json.load(json_file)
    return json_data

@pytest.fixture()
def json_unranked_content():
    test_file_path = os.path.dirname(__file__) + "\\test_unranked.json"
    with open(test_file_path, "r", encoding="utf-8") as json_file:
        json_data = json.load(json_file)
    return json_data

@pytest.fixture(autouse=True)
def no_json_dump(monkeypatch):
    monkeypatch.delattr('json.dump')
    # monkeypatch.delattr('builtins.open')

@pytest.fixture()
def scoreboard():
    return Scoreboard(data_file="test_sorted.json")

@pytest.fixture()
def scoreboard_mock(json_sorted_content):
    scoreboard = Scoreboard(None)
    scoreboard.get_scoreboard = Mock()
    scoreboard.get_scoreboard.return_value = json_sorted_content
    return scoreboard

def test_Scoreboard_import():
    from task_2_2.scoreboard import Scoreboard
    assert callable(Scoreboard), '"Scoreboard" is not callable'

def test_json_file_exists(scoreboard):
    scoreboard_path_full = sys.modules[scoreboard.__module__].__file__
    scoreboard_path_folder = os.path.dirname(scoreboard_path_full)
    assert os.path.exists(scoreboard_path_folder + "\\myfile.json")

@patch("task_2_2.scoreboard.json.load")
@patch("task_2_2.scoreboard.open")
def test_get_scoreboard_data_return(mock_open, mock_json, scoreboard, json_sorted_content):
    mock_json.return_value = json_sorted_content
    sb = scoreboard.get_scoreboard()
    assert sb == json_sorted_content

@pytest.mark.parametrize('score, expected', (
    (2, 3),
    (0, 4),
    (1, 3),
    (199, 2),
    (1000, 1),
))
def test_user_rank_valid_score(scoreboard_mock, score, expected):
    assert scoreboard_mock.get_user_rank(score) == expected

def test_user_rank_invalid_score(scoreboard_mock):
    assert scoreboard_mock.get_user_rank(-100) == 4

def test_setting_rank_by_index(scoreboard, json_sorted_content, json_unranked_content):
    json_sort = scoreboard.set_users_ranks_by_index(json_unranked_content)
    assert json_sort == json_sorted_content


@pytest.fixture()
def UserMock():
    UserMock = Mock()
    UserMock.name = Mock()
    UserMock.quizzes = Mock()
    UserMock.quizzes.all = Mock()
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
    user_score = scoreboard.get_user_score(UserMock)
    assert user_score == expected
    UserMock.quizzes.all.assert_called_once()

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
    user_score = scoreboard.get_user_score(UserMock)
    assert user_score == expected

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
    user_score = scoreboard.get_user_score(UserMock)
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
