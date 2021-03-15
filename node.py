from random import choice
from transaction import Transaction
from hashlib import sha256
from pools import VTP
import threading
from time import sleep


class Node(threading.Thread):
    def __init__(self, identities, utp, vtp, nodeName):
        threading.Thread.__init__(self)
        self.unverified = choice(list(utp.values()))
        self.sig = self.unverified.signature
        self.input = self.unverified.input
        self.output = self.unverified.output
        self.identities = identities
        self.seeninputs = []
        self.utp = utp
        self.vtp = vtp
        self.chain = []
        self.nodeName = nodeName

    def run(self):
        while (len(self.utp) > 0):
            # print(f"{self.nodeName}\nutp = {len(self.utp)} vtp = {len(self.vtp)}")
            if self.validate():
                self.update_prev()
                self.proof_of_work()
                if len(self.chain) == 0:
                    dict_pairs = self.vtp.items()
                    pairs_iterator = iter(dict_pairs)
                    genesis = next(pairs_iterator)
                    self.chain.append(genesis[0])
                else:
                    if len(self.vtp) > len(self.chain) + 1:
                        self.chain = []
                        dict_pairs = self.vtp.items()
                        pairs_iterator = iter(dict_pairs)
                        genesis = next(pairs_iterator)
                        self.chain.append(genesis[0])
                        for i in range(1, len(self.vtp)):
                            prev = list(self.vtp.items())[i]
                            prev = prev[0]
                            self.chain.append(self.vtp[prev].number)
                    else:
                        prev = list(self.vtp.items())[-1]
                        prev = prev[0]
                        if prev not in self.chain:
                            self.chain.append(self.vtp[prev].number)
            if len(self.utp) > 0:
                self.unverified = choice(list(self.utp.values()))
                self.sig = self.unverified.signature
                self.input = self.unverified.input
                self.output = self.unverified.output
        print(f"{self.nodeName}, Chain: {self.chain}, chain length = {len(self.chain)}")

           
    def validate(self):
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
                    valid = True
                    break
        for pair in self.input:
            if pair in self.seeninputs:
                # print("Error: Attempted Double Spending")
                try:
                    del self.utp[self.unverified.number]
                    return False
                except KeyError:
                    return False
            else:
                self.seeninputs.append(pair)
        for pair in self.input:
            inputcoins += pair[1]['value']
        if inputcoins < self.output['value']:
            # print("# Coins in input don't satisfy coins in output")
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
                try:
                    del self.utp[self.unverified.number]
                    self.vtp[self.unverified.number] = self.unverified
                    break
                except KeyError:
                    pass
            #Our transaction is in the VTP, so it's been mined already
            if self.unverified.number in self.vtp.keys():
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
