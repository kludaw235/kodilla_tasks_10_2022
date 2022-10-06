from task_1_2.factorization import prime_factors

def test_factorization_import():
    try:
        from task_1_2.factorization import prime_factors
        assert callable(prime_factors), '"Prime factors" is not callable'
    except ImportError as e:
        raise AssertionError(e)

def test_result_is_a_list():
    result = prime_factors(2)
    assert type(result) is list, "Result is not a list"

def test_number_is_prime():
    result = prime_factors(11)
    expected = [11]
    assert result == expected, f"Expected {expected}, got {result}"

def test_number_is_not_prime():
    result = prime_factors(12)
    expected_not = [12]
    assert result != expected_not, f"Expected not {expected_not}, got {result}"

def test_number_with_same_factors():
    result = prime_factors(32)
    expected = [2, 2, 2, 2, 2]
    assert result == expected, f'Expected {expected}, got {result}'

def test_number_with_different_factors():
    result = prime_factors(24)
    expected = [2, 2, 2, 3]
    assert result == expected, f'Expected {expected}, got {result}'

def test_big_number():
    result = prime_factors(3958159172)
    expected = [2, 2, 11, 2347, 38329]
    assert result == expected, f'Expected {expected}, got {result}'

def test_negative_number():
    try:
        result = prime_factors(-100)
        assert False, f'Expected ValueError, got {result}'
    except ValueError:
        pass

def test_zero():
    try:
        result = prime_factors(0)
        assert False, f'Expected ValueError, got {result}'
    except ValueError:
        pass

def test_one():
    try:
        result = prime_factors(1)
        assert False, f'Expected ValueError, got {result}'
    except ValueError:
        pass

def test_float_argument():
    try:
        result = prime_factors(2.5)
        assert False, f'Expected TypeError, got {result}'
    except TypeError:
        pass

def test_string_argument():
    try:
        result = prime_factors('two')
        assert False, f'Expected TypeError, got {result}'
    except TypeError:
        pass

def test_list_argument():
    try:
        result = prime_factors([2,5])
        assert False, f'Expected TypeError, got {result}'
    except TypeError:
        pass


def test_tupple_argument():
    try:
        result = prime_factors((2, 5))
        assert False, f'Expected TypeError, got {result}'
    except TypeError:
        pass


test_cases = (test_factorization_import, test_result_is_a_list, test_number_is_prime, test_number_is_not_prime,
              test_number_with_same_factors, test_number_with_different_factors, test_big_number,
              test_negative_number, test_zero, test_one, test_float_argument, test_string_argument,
              test_list_argument, test_tupple_argument)

if __name__ == '__main__':
    for test in test_cases:
        print(f'{test.__name__}: ', end="")
        try:
            test()
            print("OK")
        except AssertionError as error:
            print(error)