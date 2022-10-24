from task_2_2.modules.difficulty import Difficulty
import pytest


def test_attr_assign_name():
    diff = Difficulty(name="Test")
    assert diff.name == "Test"

@pytest.mark.parametrize('not_str', (
    2,
    2.0,
    [2,1],
    (2,1),
))
def test_attr_name_is_string(not_str):
    with pytest.raises(ValueError):
        Difficulty(name=not_str)

def test_attr_assign_multiplier():
    diff = Difficulty(points_multiplier=10)
    assert diff.points_multiplier == 10

@pytest.mark.parametrize('not_int', (
    "test",
    2.0,
    [2,1],
    (2,1),
))
def test_attr_multiplier_is_int(not_int):
    with pytest.raises(ValueError):
        Difficulty(points_multiplier=not_int)