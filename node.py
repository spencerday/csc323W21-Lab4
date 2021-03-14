from random import choice
from transaction import Transaction
from hashlib import sha256
from pools import VTP
from threading import Thread


class Node(Thread):
    def __init__(self, identities, utp, vtp):
        self.unverified = choice(list(utp.values()))
        self.sig = self.unverified.signature
        self.input = self.unverified.input
        self.output = self.unverified.output
        self.identities = identities
        self.seeninputs = []
        self.utp = utp
        self.vtp = vtp
        self.chain = []

    def run(self):
        while (len(self.utp) > 0):
            print(f"NODE\nutp = {len(self.utp)} vtp = {len(self.vtp)}")
            if self.validate():
                self.update_prev()
                self.proof_of_work()
                if len(self.chain) == 0:
                    dict_pairs = self.vtp.items()
                    pairs_iterator = iter(dict_pairs)
                    genesis = next(pairs_iterator)
                    self.chain.append(genesis)
                else:
                    prev = list(self.vtp.items())[-1]
                    prev = prev[0]
                    self.chain.append(self.vtp[prev])
            print("Current UTP State: " + str(list(self.utp.values())))
            if len(self.utp) > 0:
                self.unverified = choice(list(self.utp.values()))
                self.sig = self.unverified.signature
                self.input = self.unverified.input
                self.output = self.unverified.output
                print("Chain: " + str(self.chain))
            
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
                    print("Valid identity (N Value): " + str(hex(identity.n)))
                    valid = True
                    break
        for pair in self.input:
            if pair in self.seeninputs:
                print("Error: Attempted Double Spending")
                del self.utp[self.unverified.number]
                return False
            else:
                self.seeninputs.append(pair)
        for pair in self.input:
            inputcoins += pair[1]['value']
        if inputcoins < self.output['value']:
            print("# Coins in input don't satisfy coins in output")
            valid = False
        return valid

    def proof_of_work(self):
        nonce = 0
        while(True):
            hash = int.from_bytes(sha256(bytes(str(self.unverified.type) + str(self.input) + str(self.output)
            + str(self.sig) + str(self.unverified.number) + str(self.unverified.prev)+ str(nonce), "latin")).digest(), byteorder='big')
            if hash <= 0x00000FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF:
                self.unverified.nonce = nonce
                self.unverified.proof = hash
                #Add unverified to VTP
                #VTP[self.unverified.number] = self.unverified
                #Delete from UTP
                #TODO: Braodcast signal for other nodes to stop mining
                del self.utp[self.unverified.number]
                self.vtp[self.unverified.number] = self.unverified
                break
            nonce += 1

    def update_prev(self):
        #For first transaction, this is the hash of the genesis

        prev = list(self.vtp.items())[-1]
        prev = prev[0]
        verified = self.vtp[prev]
        hash = sha256(bytes(str(verified.type) + str(verified.input) + str(verified.output)
        + str(verified.signature) + str(verified.number) + str(verified.prev) + str(verified.nonce) + str(verified.proof), 'latin')).hexdigest()
        self.unverified.prev = hash
        #self.proof_of_work()
        #TODO: Support forks in Node's chain

        """
    def add_and_verify(self):
        for trans in VTP:
            to_verify = Node(self.identities, VTP)
            if to_verify.validate():
                print()
"""

