from random import choice
from transaction import Transaction
from hashlib import sha256
from pools import VTP

#Unverified transaction Pool
UTP = {} # Format: Transaction number: TransactionBlock


class Node:
    def __init__(self, utp, identities):
        #self.key = choice(utp.keys())
        self.utp = utp
        self.unverified = choice(list(utp.values()))
        self.sig = self.unverified.signature
        self.input = self.unverified.input
        self.output = self.unverified.output
        self.identities = identities
        self.seeninputs = []
        self.prev = None

    def validate(self):
        #TODO: Run checks for valid transactions: Signature verifies transaction, each input used once, number of coins in input matches those in output
        valid = False
        inputcoins = 0
        #if input does not yet exist, move on to next transaction
        if self.input is None:
           return False
        # For each of the 3 signatures
        for i in range(3):
            for identity in self.identities:
                hash = 0
                if i == 0:
                    hash = int.from_bytes(sha256(bytes(self.unverified.type, 'latin')).digest(), byteorder='big')
                elif i == 1:
                    hash = int.from_bytes(sha256(bytes(str(self.unverified.input), 'latin')).digest(), byteorder='big')
                else:
                    hash = int.from_bytes(sha256(bytes(str(self.unverified.output), 'latin')).digest(), byteorder='big')
                hashFromSignature = pow(self.sig[i], identity.e, identity.n)
                if hash == hashFromSignature:
                    print("Valid identity (N Value): " + str(identity.n))
                    valid = True
                    break
        for pair in self.input:
            if pair in self.seeninputs:
                print("Error: Attempted Double Spending")
                del self.utp[self.unverified.number]
                valid = False
            else:
                self.seeninputs.append(pair)
        for pair in self.input:
            inputcoins += pair[1]['value']
        if inputcoins < self.output['value']:
            print("Coins in input don't match coins in output")
            valid = False
        return valid

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
                #Add unverified to VTP
                VTP[self.unverified.number] = self.unverified
                #Delete from UTP
                del self.utp[self.unverified.number]
                break
            nonce += 1

    def update_prev(self):
        #TODO: Update previous verified transaction for an element of UTP with last item in VTP
        #For first transaction, this is the hash of the genesis
        if self.validate():
            hash = sha256(bytes(str(self.unverified.type) + str(self.input) + str(self.output)
            + str(self.sig) + str(self.unverified.number), 'latin')).hexdigest()
            self.prev = hash
            self.proof_of_work()
    #TODO: Support forks in Node's chain
