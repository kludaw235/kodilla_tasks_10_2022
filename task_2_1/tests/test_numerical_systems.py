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

class TestRomToDecGreatNums:
    def test_1(self):
        assert NSC('ROM', 'DEC', 'MDCLXV').target_number == 1665

    def test_2(self):
        assert NSC('ROM', 'DEC', 'MMMMDCCCXXXIX').target_number == 4839

    def test_3(self):
        assert NSC('ROM', 'DEC', 'MMMDCCCLXXXVIII').target_number == 3888

    def test_4(self):
        assert NSC('ROM', 'DEC', 'MMDCCLXXVIII').target_number == 2778

    def test_5(self):
        assert NSC('ROM', 'DEC', 'CMXCIX').target_number == 999


class TestSingleAppearDLV:
    def test_single_appear_D(self):
        with pytest.raises(ValueError):
            print(NSC('ROM', 'DEC', 'MDDLX').target_number)

    def test_single_appear_L(self):
        with pytest.raises(ValueError):
            print(NSC('ROM', 'DEC', 'MDLLX').target_number)

    def test_single_appear_V(self):
        with pytest.raises(ValueError):
            print(NSC('ROM', 'DEC', 'VVVI').target_number)

class TestSmallerDenominationsAsMCX:
    def test_smaller_equal_M(self):
        with pytest.raises(ValueError):
            print(NSC('ROM', 'DEC', 'CCCCCCCCCC').target_number)

    def test_smaller_exceed_M(self):
        with pytest.raises(ValueError):
            print(NSC('ROM', 'DEC', 'CCCCCCCCCCC').target_number)

    def test_smaller_correct_M(self):
        assert NSC('ROM', 'DEC', 'CCCCCCCCC').target_number == 900

    def test_smaller_equal_C(self):
        with pytest.raises(ValueError):
            print(NSC('ROM', 'DEC', 'XXXXXXXXXX').target_number)

    def test_smaller_exceed_C(self):
        with pytest.raises(ValueError):
            print(NSC('ROM', 'DEC', 'XXXXXXXXXXX').target_number)

    def test_smaller_correct_C(self):
        assert NSC('ROM', 'DEC', 'XXXXXXXXX').target_number == 90

    def test_smaller_equal_X(self):
        with pytest.raises(ValueError):
            print(NSC('ROM', 'DEC', 'IIIIIIIIII').target_number)

    def test_smaller_exceed_X(self):
        with pytest.raises(ValueError):
            print(NSC('ROM', 'DEC', 'IIIIIIIIIII').target_number)

    def test_smaller_correct_X(self):
        assert NSC('ROM', 'DEC', 'IIIIIIIII').target_number == 9
