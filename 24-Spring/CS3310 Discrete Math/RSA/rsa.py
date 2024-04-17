import random

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
        text = ""
        while number > 0:
            text = alphabet[number % base] + text
            number //= base
        return text

    def make_odd(self, n):
        if n % 2 == 0:
            n += 1
        return n

    def check_prime(self, P, iterations=20):
        if P < 2:
            return False
        if P != 2 and P % 2 == 0:
            return False  # Early return for even numbers > 2

        for i in range(iterations):
            if not self.miller_test(P):
                return False
        return True

    def miller_test(self, P):
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

    def find_next_prime(self, n):
        while not self.check_prime(n):
            n += 2  # Optionally adjust to add larger gaps
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

    def generate_keys(self, text1, text2):
        p = self.text_to_number(text1, self.alphabet1)
        q = self.text_to_number(text2, self.alphabet1)
        """ print("Converted p:", p)
        print("Converted q:", q) """

        if p < 10**200 or q < 10**200:
            print("Error: Input strings are too short.")
            return

        p = p % (10**200)
        q = q % (10**200)
        """ print("Modulo p:", p)
        print("Modulo q:", q) """

        p = self.make_odd(p)
        q = self.make_odd(q)
        """ print("Made odd p:", p)
        print("Made odd q:", q) """

        p = self.find_next_prime(p)
        q = self.find_next_prime(q)
        """ print("Prime p:", p)
        print("Prime q:", q) """

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

        print("Files generated successfully.")

    def encrypt(self, inputfile, outputfile):
        # Read the input file
        with open(inputfile, "rb") as fin:
            PlainTextBinary = fin.read()
        PlainText = PlainTextBinary.decode("utf-8")

        # Read n and e from public.txt
        with open("public.txt", "r") as pub_file:
            n = int(pub_file.readline().strip())
            e = int(pub_file.readline().strip())

        # Process the plaintext in blocks
        block_size = 216
        blocks = [PlainText[i:i + block_size] for i in range(0, len(PlainText), block_size)]

        # Convert blocks to numbers, encrypt, and convert back to base 70 text
        encrypted_blocks = []
        for block in blocks:
            block_number = self.text_to_number(block, self.alphabet2)
            encrypted_number = pow(block_number, e, n)  # RSA encryption
            encrypted_text = self.number_to_text(encrypted_number, self.alphabet2) + '$'
            encrypted_blocks.append(encrypted_text)

        # Write the encrypted blocks to the output file
        with open(outputfile, "wb") as fout:
            for encrypted_text in encrypted_blocks:
                fout.write(encrypted_text.encode("utf-8"))

    def decrypt(self, inputfile, outputfile):
        # Read the input file
        with open(inputfile, "rb") as fin:
            encrypted_text = fin.read().decode("utf-8")
        
        # Read n and d from private.txt
        with open("private.txt", "r") as priv_file:
            n = int(priv_file.readline().strip())
            d = int(priv_file.readline().strip())
        
        # Split the encrypted text into blocks using $ as a delimiter
        encrypted_blocks = encrypted_text.split('$')
        
        # Remove any empty strings that might have been added due to trailing $
        encrypted_blocks = [block for block in encrypted_blocks if block]

        # decrypt each block
        decrypted_blocks = []
        for block in encrypted_blocks:
            block_number = self.text_to_number(block, self.alphabet2)
            decrypted_number = pow(block_number, d, n)  # RSA decryption
            decrypted_text = self.number_to_text(decrypted_number, self.alphabet2)
            decrypted_blocks.append(decrypted_text)
        
        # Write the decrypted text to the output file
        with open(outputfile, "wb") as fout:
            for decrypted_text in decrypted_blocks:
                fout.write(decrypted_text.encode("utf-8"))

def main():
    rsa = RSA()

    """ # Generate keys using two very long strings
    long_string1 = "x" * 300  # Example long string of repeated 'x's
    long_string2 = "y" * 300  # Example long string of repeated 'y's
    rsa.generate_keys(long_string1, long_string2) """

    input_filename = "HaydenEncrypted.txt"
    decrypted_filename = "decrypted_output.txt"
    rsa.decrypt(input_filename, decrypted_filename)

if __name__ == "__main__":
    main()
