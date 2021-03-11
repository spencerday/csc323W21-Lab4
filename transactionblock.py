from hashlib import sha256
import json
from random import choice
from Crypto.PublicKey import RSA

TYPES = ["trans", "join", "merge"]

class TransactionBlock:
    #TODO: Write method to read a transaction from json TransactionFile and populate all values here except prev, nonce, and proof for all transactions
    def __init__(self, type, input, output, signature, number):
        self.type = type
        self.input = input
        self.output = output
        self.signature = signature
        self.number = number
        self.prev = None
        self.nonce = None
        self.proof = None

    def JSON(self):
        return json.dumps(self.__dict__, indent=4, separators=(",", ": "))


if __name__ == '__main__':
    alice = RSA.generate(bits=1024)
    bob = RSA.generate(bits=1024)


