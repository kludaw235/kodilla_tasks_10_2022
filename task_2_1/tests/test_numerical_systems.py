import pytest
from task_2_1.numerical_systems import NumericalSystemsConverter as NSC

def test_NumericalSystemsConverter_import():
    try:
        from task_2_1.numerical_systems import NumericalSystemsConverter
        assert callable(NumericalSystemsConverter), '"NumericalSystemsConverter" is not callable'
    except ImportError as e:
        raise AssertionError(e)

def test_3args_validation():
    try:
        NSC("ROM", "DEC", "IV")
    except Exception as e:
        assert False, f"3 arguments raised an exception: {e}"