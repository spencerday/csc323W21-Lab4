from random import choice
from transaction import Transaction

#Unverified transaction Pool
UTP = {}
VTP = {}

class Node:
    def __init__(self):
        self.unverified = choice(UTP.keys())
        self.sig = UTP[self.unverified].signature
        self.input = UTP[self.unverified].input
        self.output = UTP[self.unverified].output

    def validate(self):
        #TODO: Run checks for valid transactions: Signature verifies transaction, each input used once, number of coins in input matches those in output
        print()
    def proof_of_work(self):
        #TODO: Loop randomly chooses nonce, appends to serialized version of transaction, and hash until
        # hash <= 0x00000FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF
        print()
    def update_prev(self):
        #TODO: Update previous verified transaction for an element of UTP with last item in VTP
        #For first transaction, this is the hash of the genesis
        print()
    #TODO: Support forks in Node's chain
