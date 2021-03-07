from hashlib import sha256
import json
from random import choice
from Crypto.PublicKey import RSA

TYPES = ["trans", "join", "merge"]

class ZCTransaction:
    def __init__(self, inputs, prev):
        self.type = choice(TYPES)
        self.input = inputs
        self.output = []
        self.keyPair = RSA.generate(bits=1024)
        self.signature = [
            pow(int.from_bytes(sha256(bytes(self.type, 'latin')).digest(), byteorder='big'), self.keyPair.d, self.keyPair.n),
            pow(int.from_bytes(sha256(bytes(self.input, 'latin')).digest(), byteorder='big'), self.keyPair.d, self.keyPair.n),
            pow(int.from_bytes(sha256(bytes(self.output, 'latin')).digest(), byteorder='big'), self.keyPair.d, self.keyPair.n),
        ]
        self.number = sha256(bytes(str(self.input) + str(self.output) + str(self.signature), 'latin')).hexdigest()
        self.prev = prev
        self.nonce = None
        self.proof = None
    def JSON(self):
        return json.dumps(self.__dict__, indent=4, separators=(",", ": "))





if __name__ == '__main__':
    testblock = ZCTransaction()

