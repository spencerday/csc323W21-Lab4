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

    def __init__(self, type, input, output, identity):
        """
        Parameters:
            inputs - set containing transaction numbers
            outputs - a set of dicts in the form {"value": value, "key": (pubkey.n, pubKey.e)}
            identity - RSA object
        """
        self.type = type
        self.input = inputs
        self.output = outputs
        self.signature = [
            pow(int.from_bytes(sha256(bytes(self.type, 'latin')).digest(), byteorder='big'), identity.d, identity.n),
            pow(int.from_bytes(sha256(bytes(str(self.input), 'latin')).digest(), byteorder='big'), identity.d, identity.n),
            pow(int.from_bytes(sha256(bytes(str(self.output), 'latin')).digest(), byteorder='big'), identity.d, identity.n),
        ]
        self.number = sha256(bytes(str(self.input) + str(self.output)
            + str(self.signature), "latin")).hexdigest()

    def JSON(self):
        """
        Returns string to be put in a JSON file
        """
        return json.dumps(self.__dict__, indent=4, separators=(",", ": "))
