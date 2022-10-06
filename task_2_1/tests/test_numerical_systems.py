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

def test_rom_to_dec_returns_int():
    assert isinstance(NSC("ROM", "DEC", "IV").target_number, int)

class TestRomToDecSmallNums:
    def test_1(self):
        assert NSC('ROM', 'DEC', 'IV').target_number == 4

    def test_2(self):
        assert NSC('ROM', 'DEC', 'XXIV').target_number == 24

    def test_3(self):
        assert NSC('ROM', 'DEC', 'XXXVI').target_number == 36

    def test_4(self):
        assert NSC('ROM', 'DEC', 'XIIIIII').target_number == 16

    def test_5(self):
        assert NSC('ROM', 'DEC', 'XXIX').target_number == 29