from hashlib import sha256
import json
from random import choice
from Crypto.PublicKey import RSA

TYPES = ["trans", "join", "merge"]

class ZCTransaction:
    def __init__(self, type, identity, inputs, prev):
        self.type = type
        self.input = inputs
        self.output = []
        self.keyPair = identity
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
    def read_json(self, filename):
        with open(filename) as f:
            data = json.load(f)
        return data





if __name__ == '__main__':
    alice = RSA.generate(bits=1024)
    bob = RSA.generate(bits=1024)
    john = RSA.generate(bits=1024)
    max = RSA.generate(bits=1024)
    spencer = RSA.generate(bits=1024)

    print(f"Alice Public key:  (n={hex(alice.n)}, e={hex(alice.e)})")
    print(f"Alice Private key: (n={hex(alice.n)}, d={hex(alice.d)})")

    print(f"Bob Public key:  (n={hex(bob.n)}, e={hex(bob.e)})")
    print(f"Bob Private key: (n={hex(bob.n)}, d={hex(bob.d)})")

    print(f"John Public key:  (n={hex(john.n)}, e={hex(john.e)})")
    print(f"John Private key: (n={hex(john.n)}, d={hex(john.d)})")

    print(f"Max Public key:  (n={hex(max.n)}, e={hex(max.e)})")
    print(f"Max Private key: (n={hex(max.n)}, d={hex(max.d)})")

    print(f"Spencer Public key:  (n={hex(spencer.n)}, e={hex(spencer.e)})")
    print(f"Spencer Private key: (n={hex(spencer.n)}, d={hex(spencer.d)})")

    #testblock = ZCTransaction()
    #genesis_block = ZCTransaction('trans', None)

