from hashlib import sha256
import json
from random import choice
from Crypto.PublicKey import RSA

TYPES = ["trans", "join", "merge"]

class TransactionBlock:
    #TODO: Write method to read a transaction from json TransactionFile and populate all values here except prev, nonce, and proof for all transactions
    def __init__(self, transaction):
        self.type = transaction.type
        self.input = transaction.input
        self.output = transaction.output
        self.signature = transaction.signature
        self.number = transaction.number
        self.prev = None
        self.nonce = None
        self.proof = None
    def JSON(self):
        return json.dumps(self.__dict__, indent=4, separators=(",", ": "))
    def read_json(self, filename):
        with open(filename) as f:
            data = json.load(f)
        print(data)


if __name__ == '__main__':
    alice = RSA.generate(bits=1024)
    bob = RSA.generate(bits=1024)


