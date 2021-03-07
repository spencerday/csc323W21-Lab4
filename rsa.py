from Crypto.Util.number import getPrime


class RSA:
    """
    Implementation of RSA
    """
    def __init__(self, keyLen=2048):
        self.e = 65537
        self.p = getPrime(keyLen)
        self.q = getPrime(keyLen)
        self.phi = ((self.p - 1) * (self.q - 1)) // self.gcd(self.p - 1, self.q - 1)
        self.coprimeCheck(keyLen)
        self.n = self.p * self.q
        self.d = self.modMultInv(self.e, self.phi)

    def coprimeCheck(self, keyLen):
        """
        Make sure that the primes are coprime to self.e
        """
        while self.gcd(self.e, self.phi) != 1:
            self.p = getPrime(keyLen)
            self.q = getPrime(keyLen)

    def gcd(self, x, y):
        """
        Find greatest common denominator using Euclidiean algorithm
        """
        r = x % y

        while r:
            x = y
            y = r
            r = x % y

        return y

    def gcdExtended(self, x, y):
        """
        Extended version of Euclidiean algorithm
        """
        if x % y == 0:
            return (y, 0, 1)

        gcd, c1, c2 = self.gcdExtended(y, x % y)
        c1 -= x // y * c2
        return (gcd, c2, c1)

    def modMultInv(self, x, y):
        """
        Manually calculates modular multiplicative inverse
        """
        gcd, c1, c2 = self.gcdExtended(x, y)

        if gcd != 1:
            print("No modular multiplicative inverse")
            return
        else:
            return c1 % y

    def getPublicKey(self):
        """
        Getter function for public key
        """
        return (self.e, self.n)

    def getPrivateKey(self):
        """
        Getter function for private key
        """
        return (self.d, self.n)

    def sign(self, m):
        """
        RSA encryption
        """
        return pow(m, self.e, self.n)

    def verify(self, c):
        """
        RSA decryption
        """
        return pow(c, self.d, self.n)


def asciiToInt(message):
    """
    Converts a string to an int that can be used to encrypt
    """
    messageBytes = message.encode(encoding='utf-8')
    messageHex = messageBytes.hex()
    return int(messageHex, 16)
