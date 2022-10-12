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


@pytest.mark.parametrize('rom_value, expected', (
        ('IV', 4),
        ('XXIV', 24),
        ('XXXVI', 36),
        ('XIIIIII', 16),
        ('XXIX', 29)))
def test_rom_to_dec_small_nums(rom_value, expected):
    assert NSC('ROM', 'DEC', rom_value).target_number == expected


@pytest.mark.parametrize('rom_value, expected', (
        ('MDCLXV', 1665),
        ('MMMMDCCCXXXIX', 4839),
        ('MMMDCCCLXXXVIII', 3888),
        ('MMDCCLXXVIII', 2778),
        ('CMXCIX', 999)))
def test_rom_to_dec_big_nums(rom_value, expected):
    assert NSC('ROM', 'DEC', rom_value).target_number == expected


@pytest.mark.parametrize('rom_value, expected_failure', (
        ('MDDLX', ValueError),
        ('MDLLX', ValueError),
        ('VVVI', ValueError)))
def test_single_appear_DLV(rom_value, expected_failure):
    with pytest.raises(expected_failure):
        print(NSC('ROM', 'DEC', rom_value).target_number)


@pytest.mark.parametrize('rom_value, expected_failure', (
        ('CCCCCCCCCC', ValueError),
        ('CCCCCCCCCCC', ValueError),
        ('XXXXXXXXXX', ValueError),
        ('XXXXXXXXXXX', ValueError),
        ('IIIIIIIIII', ValueError),
        ('IIIIIIIIIII', ValueError)))
def test_denomination_exceed_equal_MCX(rom_value, expected_failure):
    with pytest.raises(expected_failure):
        print(NSC('ROM', 'DEC', rom_value).target_number)


@pytest.mark.parametrize('rom_value, expected', (
        ('CCCCCCCCC', 900),
        ('XXXXXXXXX', 90),
        ('IIIIIIIII', 9)))
def test_denomination_correct_MCX(rom_value, expected):
    assert NSC('ROM', 'DEC', rom_value).target_number == expected


@pytest.mark.parametrize('sub_numeral, expected_results', (
        ('I', [ValueError, ValueError, ValueError, ValueError, 9, 4, 2]),
        ('X', [ValueError, ValueError, 90, 40, 20, 15, 11]),
        ('C', [900, 400, 200, 150, 110, 105, 101])))
def test_sub_leading_IXC(sub_numeral, expected_results):
    following_values = ['M', 'D', 'C', 'L', 'X', 'V', 'I']
    for i in range(len(following_values)):
        if expected_results[i] in Exception.__subclasses__():
            with pytest.raises(expected_results[i]):
                print(NSC('ROM', 'DEC', sub_numeral + following_values[i]).target_number)
        else:
            assert NSC('ROM', 'DEC', sub_numeral + following_values[i]).target_number == expected_results[i]


@pytest.mark.parametrize('sub_numeral, expected_failure, following_values', (
        ('II', ValueError, ['M', 'D', 'C', 'L', 'X', 'V']),
        ('XX', ValueError, ['M', 'D', 'C', 'L']),
        ('CC', ValueError, ['M', 'D'])))
def test_single_sub_leading_IXC(sub_numeral, expected_failure, following_values):
    for i in range(len(following_values) - 1):
        with pytest.raises(expected_failure):
            print(NSC('ROM', 'DEC', sub_numeral + following_values[i]).target_number)


@pytest.mark.parametrize('rom_value, expected_failure', (
        ('IVX', ValueError),
        ('XLC', ValueError),
        ('CDM', ValueError),
        ('IVXLCDM', ValueError)))
def test_descending_order(rom_value, expected_failure):
    with pytest.raises(expected_failure):
        print(NSC('ROM', 'DEC', rom_value).target_number)


def test_small_letters():
    assert NSC('ROM', 'DEC', 'mdclxvi').target_number == 1666


def test_dec_to_rom_target_str():
    assert isinstance(NSC('DEC', 'ROM', 4).target_number, str)


@pytest.mark.parametrize('dec_value, expected', (
        (33, 'XXXIII'),
        (79, 'LXXIX'),
        (44, 'XLIV'),
        (66, 'LXVI'),
        (1, 'I')))
def test_dec_to_rom_small_nums(dec_value, expected):
    assert NSC('DEC', 'ROM', dec_value).target_number == expected


@pytest.mark.parametrize('dec_value, expected', (
        (1665, 'MDCLXV'),
        (4444, 'MMMMCDXLIV'),
        (3888, 'MMMDCCCLXXXVIII'),
        (2778, 'MMDCCLXXVIII'),
        (4999, 'MMMMCMXCIX')))
def test_dec_to_rom_big_nums(dec_value, expected):
    assert NSC('DEC', 'ROM', dec_value).target_number == expected


@pytest.mark.parametrize('test, input, expected_failure', (
        ('Test float', 2.5, ValueError),
        ('Test list', [2, 5], ValueError),
        ('Test tuple', (2, 5), ValueError),
        ('Test negative', -1, ValueError),
        ('Test zero', 0, ValueError)))
def test_dec_to_rom_input_validation(test, input, expected_failure):
    with pytest.raises(expected_failure):
        print(NSC('DEC', 'ROM', input).target_number, test)


def test_src_str():
    assert NSC('DEC', 'ROM', '4').target_number == 'IV'
