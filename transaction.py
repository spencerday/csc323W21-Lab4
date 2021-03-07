import json
from random import choice
from hashlib import sha256
from Crypto.PublicKey import RSA
from random import randint


TYPES = ["trans", "join", "merge"]


class Transaction:
    """
    Class used to generate random transactions
    """

    def __init__(self, inputs, outputs, identity):
        """
        Parameters:
            inputs - set containing transaction numbers
            outputs - a set of dicts in the form {"value" : value, "key" : pubKey"}
            identity - RSA object
        """
        self.type = choice(TYPES)
        self.input = inputs
        self.output = outputs
        self.signature = [
            pow(int.from_bytes(sha256(bytes(self.type, 'latin')).digest(), byteorder='big'), self.keyPair.d, self.keyPair.n),
            pow(int.from_bytes(sha256(bytes(self.input, 'latin')).digest(), byteorder='big'), self.keyPair.d, self.keyPair.n),
            pow(int.from_bytes(sha256(bytes(self.output, 'latin')).digest(), byteorder='big'), self.keyPair.d, self.keyPair.n),
        ]
        self.number = sha256(bytes(str(self.INPUT) + str(self.OUTPUT)
            + str(self.SIGNATURE), "latin")).hexdigest()

    def JSON(self):
        """
        Returns string to be put in a JSON file
        """
        return json.dumps(self.__dict__, indent=4, separators=(",", ": "))
