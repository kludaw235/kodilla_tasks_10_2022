def prime_factors(number):
    factors = []
    prime = True
    for i in range(1, number+1):
        if number % i == 0:
            if number / i == 1 or number / i == number:
                pass
            else:
                prime = False
    if prime:
        factors.append(number)
    return factors