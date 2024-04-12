import random
from math import gcd, log

class RSA:
    def __init__(self):
        self.alphabet1 = "abcdefghijklmnopqrstuvwxyz"
        self.alphabet2 = ".,?! \t\n\rabcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"

    def text_to_number(self, text, alphabet):
        base = len(alphabet)
        number = 0
        for char in text:
            number = number * base + alphabet.index(char)
        return number

    def number_to_text(self, number, alphabet):
        base = len(alphabet)
        if number == 0:
            return alphabet[0]
        result = []
        while number > 0:
            result.append(alphabet[number % base])
            number = number // base
        return ''.join(reversed(result))

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

    def find_prime(self, start):
        while not self.is_prime(start):
            start += 2
        return start

    def inverse(self, a, n):
        t, newt = 0, 1
        r, newr = n, a
        while newr != 0:
            quotient = r // newr
            t, newt = newt, t - quotient * newt
            r, newr = newr, r - quotient * newr
        if r > 1:
            return None
        if t < 0:
            t += n
        return t

    def GenerateKeys(self, text1, text2):
        p = self.text_to_number(text1, self.alphabet1) % (10**200)
        q = self.text_to_number(text2, self.alphabet1) % (10**200)
        if p < 10**200 or q < 10**200:
            print("Error: Input strings are too short.")
            return
        
        p = self.find_prime(p | 1)
        q = self.find_prime(q | 1)
        
        n = p * q
        r = (p-1) * (q-1)
        e = 10**398 + 1
        while gcd(e, r) != 1:
            e += 1
        
        d = self.inverse(e, r)
        if d is None:
            print("Error: e has no modular inverse under modulo r.")
            return
        
        with open('public.txt', 'w') as f:
            f.write(f"{n}\n{e}\n")
        with open('private.txt', 'w') as f:
            f.write(f"{n}\n{d}\n")

    def Encrypt(self, inputfile, outputfile):
        with open(inputfile, "rb") as fin:
            PlainTextBinary = fin.read()
        PlainText = PlainTextBinary.decode("utf-8")
        block_size = int(log(10**400, 70))
        blocks = [PlainText[i:i+block_size] for i in range(0, len(PlainText), block_size)]
        
        n, e = map(int, open('public.txt').read().strip().split())
        
        encrypted_blocks = []
        for block in blocks:
            m = self.text_to_number(block, self.alphabet2)
            c = pow(m, e, n)
            encrypted_blocks.append(self.number_to_text(c, self.alphabet2) + "$")
        
        with open(outputfile, "wb") as fout:
            for block in encrypted_blocks:
                fout.write(block.encode("utf-8"))

    def Decrypt(self, inputfile, outputfile):
        with open(inputfile, "rb") as fin:
            encrypted_text = fin.read().decode("utf-8").split('$')
        n, d = map(int, open('private.txt').read().strip().split())
        
        decrypted_blocks = []
        for block in encrypted_text:
            if block:
                c = self.text_to_number(block, self.alphabet2)
                m = pow(c, d, n)
                decrypted_blocks.append(self.number_to_text(m, self.alphabet2))
        
        with open(outputfile, "wb") as fout:
            for block in decrypted_blocks:
                fout.write(block.encode("utf-8"))

    def main(self):
        # Assuming you provide two very long strings for text1 and text2
        text1 = "a"*250  # Placeholder: Use appropriate long strings
        text2 = "b"*250  # Placeholder
        self.GenerateKeys(text1, text2)
        input_text = self.alphabet2 * 5  # A simple repetition to make sure it's long enough
        with open('plaintext.txt', 'w') as f:
            f.write(input_text)
        self.Encrypt('plaintext.txt', 'encrypted.txt')
        self.Decrypt('encrypted.txt', 'decrypted.txt')

# Create an RSA instance and run the main function
rsa = RSA()
rsa.main()
