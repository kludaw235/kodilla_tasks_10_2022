def prime_factors(number):
    if number <= 1:
        raise ValueError()
    elif not isinstance(number, int):
        raise TypeError()

    factors = []
    i = 1
    while number != i:
        i += 1
        while True:
            if number / i != 1 and number % i == 0:
                number = number // i
                factors.append(i)
                continue
            break
    factors.append(number)
    return factors