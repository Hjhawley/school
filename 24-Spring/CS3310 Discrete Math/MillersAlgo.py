import random

def isMillerPrime(P, iterations=20):
    if P < 2:
        return False
    if P != 2 and P % 2 == 0:
        return False  # Early return for even numbers > 2

    for _ in range(iterations):
        if not millerTest(P):
            return False  # Definitely composite (not prime)
    return True  # Almost certainly prime

def millerTest(P):
    T = P - 1
    S = 0
    while T % 2 == 0:
        T //= 2
        S += 1

    b = random.randrange(2, P)
    x = pow(b, T, P)
    if x == 1 or x == P - 1:
        return True

    for _ in range(S - 1):
        x = pow(x, 2, P)
        if x == P - 1:
            return True
    return False

def isPrime(P):
    if P < 2:
        return False
    for i in range(2, int(P**0.5) + 1):
        if P % i == 0:
            return False
    return True

def checkPrime(P):
    if isPrime(P) and isMillerPrime(P):
        return True
    else:
        return False

# Example
P = 6972593
print(f"{P} is {'prime' if checkPrime(P) else 'not prime'}")
