class RSA:
    def __init__(self):
        self.alphabet1 = "abcdefghijklmnopqrstuvwxyz"

    def text_to_number(self, text):
        base = len(self.alphabet1)
        number = 0
        for char in text:
            number = number * base + self.alphabet1.index(char)
        return number

    def make_odd(self, n):
        if n % 2 == 0:
            n += 1
        return n

    def is_prime(self, n):
        if n <= 1:
            return False
        if n <= 3:
            return True
        if n % 2 == 0 or n % 3 == 0:
            return False
        i = 5
        while i * i <= n:
            if n % i == 0 or n % (i + 2) == 0:
                return False
            i += 6
        return True

    def find_next_prime(self, n):
        while not self.is_prime(n):
            n += 2
        return n

    def gcd(self, a, b):
        while b != 0:
            a, b = b, a % b
        return a

    def inverse(self, a, n):
        t, newt = 0, 1
        r, newr = n, a
        while newr != 0:
            quotient = r // newr
            t, newt = newt, t - quotient * newt
            r, newr = newr, r - quotient * newr
        if r > 1:
            return "a is not invertible"
        if t < 0:
            t += n
        return t

    def GenerateKeys(self, text1, text2):
        p = self.text_to_number(text1)
        q = self.text_to_number(text2)

        if p < 10**200 or q < 10**200:
            print("Error: Input strings are too short.")
            return

        p = p % (10**200)
        q = q % (10**200)

        p = self.make_odd(p)
        q = self.make_odd(q)

        p = self.find_next_prime(p)
        q = self.find_next_prime(q)

        n = p * q
        r = (p - 1) * (q - 1)

        e = 10**398 + 1
        while self.gcd(e, r) != 1:
            e += 2

        d = self.inverse(e, r)

        with open("public.txt", "w") as pub_file:
            pub_file.write(f"{n}\n{e}\n")

        with open("private.txt", "w") as priv_file:
            priv_file.write(f"{n}\n{d}\n")

# Usage:
# rsa = RSA()
# rsa.GenerateKeys("your_prime_string1", "your_prime_string2")
