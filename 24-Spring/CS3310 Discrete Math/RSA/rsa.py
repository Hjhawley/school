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

    def Encrypt(self, inputfile, outputfile):
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

    def Decrypt(self, inputfile, outputfile):
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

        # Decrypt each block
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

# rsa = RSA()
# rsa.GenerateKeys("your_prime_string1", "your_prime_string2")
# rsa.Encrypt("input.txt", "output.txt")
