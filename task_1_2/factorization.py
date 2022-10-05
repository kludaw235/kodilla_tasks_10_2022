def prime_factors(number):
    factors = []
    for i in range(1, number+1):
        if number % i == 0:
            while True:
                if number / i == 1 or number / i == number:
                    pass
                else:
                    number = number // i
                    factors.append(i)
                    continue
                break
    factors.append(number)
    return factors