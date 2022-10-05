

def test_factorization_import():
    try:
        from task_1_2.factorization import prime_factors
        assert callable(prime_factors), '"Prime factors" is not callable'
    except ImportError as e:
        raise AssertionError(e)


test_cases = (test_factorization_import, )

if __name__ == '__main__':
    for test in test_cases:
        print(f'{test.__name__}: ', end="")
        try:
            test()
            print("OK")
        except AssertionError as error:
            print(error)
