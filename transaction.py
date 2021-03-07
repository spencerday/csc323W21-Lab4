import json
from random import choice
from hashlib import sha256
from rsa import RSA, asciiToInt


TYPES = ["trans", "join", "merge"]


class Transaction:
    """
    Class used to generate random transactions
    """

    def __init__(self, inputs):
        """
        Parameters:
            inputs - set containing transaction numbers
        """
        self.TYPE = choice(TYPES)
        self.INPUT = inputs
        self.OUTPUT = self.getOutput(self.INPUT)
        rsa = RSA()  # for creating signatures
        self.SIGNATURE = [
            rsa.sign(asciiToInt(self.TYPE)),
            rsa.sign(asciiToInt(str(self.INPUT))),
            rsa.sign(asciiToInt(str(self.OUTPUT)))
        ]
        self.NUMBER = sha256(bytes(str(self.INPUT) + str(self.OUTPUT)
            + str(self.SIGNATURE), "latin")).hexdigest()

    def getOutput(self, inputs):
        """
        Generates the outputs of (value:public key) pairs
        """
        #TODO: generate the pairs for each input

    def JSON(self):
        """
        Returns string to be put in a JSON file
        """
        return json.dumps(self.__dict__, indent=4, separators=(",", ": "))
