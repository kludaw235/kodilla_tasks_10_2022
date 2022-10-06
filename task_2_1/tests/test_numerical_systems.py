import pytest

def test_NumericalSystemsConverter_import():
    try:
        from task_2_1.numerical_systems import NumericalSystemsConverter
        assert callable(NumericalSystemsConverter), '"NumericalSystemsConverter" is not callable'
    except ImportError as e:
        raise AssertionError(e)
