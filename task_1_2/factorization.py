def prime_factors(number):
    if number <= 1:
        raise ValueError
    factors = []
    i = 0
    while True:
        i += 1
        while True:
            if number / i == 1 or number / i == number:
                pass
            elif number % i == 0:
                number = number // i
                factors.append(i)
                continue
            break
        if number == i:
            break
    factors.append(number)
    return factors