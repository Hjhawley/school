import random

def checkPrime(P, iterations=20):
    if P < 2:
        return False
    if P != 2 and P % 2 == 0:
        return False  # Early return for even numbers > 2

    for i in range(iterations):
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

def main():
    while True:
        try:
            n = int(input("Give me an integer larger than 2.\n"))
            print(f"{n} is {'prime.' if checkPrime(n) else 'not prime.'}\n")
        except:
            print("Not a valid integer.\n")

if __name__ == "__main__":
    main()