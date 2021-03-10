from random import choice
from transaction import Transaction
from hashlib import sha256

#Unverified transaction Pool
UTP = {} #Format: Transaction number: TransactionBlock
VTP = {}

class Node:
    def __init__(self):
        self.key = choice(UTP.keys())
        self.unverified = UTP[self.key]
        self.sig = self.unverified.signature
        self.input = self.unverified.input
        self.output = self.unverified.output
        self.seeninputs = []

    def validate(self, identities):
        #TODO: Run checks for valid transactions: Signature verifies transaction, each input used once, number of coins in input matches those in output
        valid = False
        #For each of the 3 signatures
        for i in range(3):
            for identity in identities:
                hash = 0
                if i == 0:
                    hash = int.from_bytes(sha256(self.unverified.type).digest(), byteorder='big')
                elif i == 1:
                    hash = int.from_bytes(sha256(self.unverified.input).digest(), byteorder='big')
                else:
                    hash = int.from_bytes(sha256(self.unverified.output).digest(), byteorder='big')
                hashFromSignature = pow(self.sig[i], identity.e, identity.n)
                if hash == hashFromSignature:
                    print("Valid identity (N Value): " + str(identity.n))
                    break
        if self.input[1] in self.seeninputs:
            print("Error: Attempted Double Spending")
            del UTP[self.key]
            valid = False
        else:
            self.seeninputs.append(self.input[1])




    def proof_of_work(self):
        #TODO: Loop randomly chooses nonce, appends to serialized version of transaction, and hash until
        # hash <= 0x00000FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF
        nonce = 0
        while(True):
            hash = sha256(bytes(str(self.unverified.type) + str(self.input) + str(self.output)
            + str(self.sig) + str(self.unverified.number) + str(nonce), "latin")).hexdigest()
            if hash <= 0x00000FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF:
                self.unverified.nonce = nonce
                self.unverified.proof = hash
                break
            nonce += 1

        print()
    def update_prev(self):
        #TODO: Update previous verified transaction for an element of UTP with last item in VTP
        #For first transaction, this is the hash of the genesis
        print()
    #TODO: Support forks in Node's chain
