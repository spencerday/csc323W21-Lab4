import json
from time import sleep
from hashlib import sha256
from node import Node
from transactionblock import TransactionBlock
from transaction import Transaction
from Crypto.PublicKey import RSA
from random import choice, randint
from pools import VTP
import pools

FILE = "TransactionFile.json"
UTP = {}

def readValidTransactionFile():
    """
    Returns a list where each element is a dictionary representation of a transaction
    in the Transaction File
    """
    utp = {}

    with open('ValidTransactionFile.json', "r") as f:
        transactions = [json.loads(t) for t in f.read()[:-2].split("$")]

    for t in transactions:
        trans = TransactionBlock(t["type"],
                                 t["input"],
                                 t["output"],
                                 t["signature"],
                                 t["number"])
        utp[trans.number] = trans

    return utp

def generate_random_output(identities):
    #TODO: Generate output to two identities
    identity = choice(identities)
    value = randint(1,10)
    return {value: (hex(identity.n), hex(identity.e))}


def generate_valid_output(identity):
    return {"value": 5, "key": (hex(identity.n), hex(identity.e))}


def generate_genesis_output(identities):
    identity1 = identities[0]
    return {"value":25 , "key":(hex(identity1.n), hex(identity1.e))}
    # identity2 = identities[3]
    # outputs = []
    # outputs.append({15: (hex(identity1.n), hex(identity1.e))})
    # outputs.append({10: (hex(identity2.n), hex(identity2.e))})


def main():
    # Generates 5 static identities to populate transaction file
    alice = RSA.generate(bits=1024)
    bob = RSA.generate(bits=1024)
    john = RSA.generate(bits=1024)
    max = RSA.generate(bits=1024)
    spencer = RSA.generate(bits=1024)
    identities = [alice, bob, john, max, spencer]

    # Genesis transaction
    #transactions = [Transaction(None, generate_genesis_output(identities), identities[0])]

    # Set of 10 valid transactions
    # Alice has 25 coins
    all_valid_transactions = [Transaction('trans', None, generate_genesis_output(identities), identities[0])]
    # Alice sends 5 coins to Bob
    all_valid_transactions.append(
        Transaction('trans', [[all_valid_transactions[0].number, all_valid_transactions[0].output]],
                    generate_valid_output(identities[1]),
                    identities[0]))
    # Bob sends 5 coins to John
    all_valid_transactions.append(
        Transaction('trans', [[all_valid_transactions[1].number, all_valid_transactions[1].output]],
                    generate_valid_output(identities[2]),
                    identities[1]))
    # John sends 5 coins to Max
    all_valid_transactions.append(
        Transaction('trans', [[all_valid_transactions[2].number, all_valid_transactions[2].output]],
                    generate_valid_output(identities[3]),
                    identities[2]))
    # max sends 5 coins to Spencer
    all_valid_transactions.append(
        Transaction('trans', [[all_valid_transactions[3].number, all_valid_transactions[3].output]],
                    generate_valid_output(identities[4]),
                    identities[3]))
    # Spencer sends 5 coins to Max
    all_valid_transactions.append(
        Transaction('trans', [[all_valid_transactions[4].number, all_valid_transactions[4].output]],
                    generate_valid_output(identities[3]),
                    identities[4]))
    # Max sends 5 coins to John
    all_valid_transactions.append(
        Transaction('trans', [[all_valid_transactions[5].number, all_valid_transactions[5].output]],
                    generate_valid_output(identities[2]),
                    identities[3]))
    # Spencer double spends 5 coins to Bob
    all_valid_transactions.append(
        Transaction('trans', [[all_valid_transactions[4].number, all_valid_transactions[4].output]],
                    generate_valid_output(identities[1]),
                    identities[4]))
    # Max receives 5 coins from Spencer, 5 coins from John
    all_valid_transactions.append(
        Transaction('join', [[all_valid_transactions[3].number, all_valid_transactions[3].output],
                             [all_valid_transactions[5].number, all_valid_transactions[5].output]],
                    {'value': 10, 'key':(hex(identities[3].n), hex(identities[3].e))},
                    identities[3]))
    # Alice sends 4 coins to Bob
    all_valid_transactions.append(
        Transaction('trans', [[all_valid_transactions[0].number, all_valid_transactions[0].output]],
                    {'value': 4 , 'key':(hex(identities[1].n), hex(identities[1].e))},
                    identities[0]))
    # Bob receives payments of 5 and 4 coins from Alice
    all_valid_transactions.append(Transaction('merge',
                                              [[all_valid_transactions[1].number, all_valid_transactions[1].output],
                                               [all_valid_transactions[9].number, all_valid_transactions[9].output]],
                                              generate_valid_output(identities[1]),
                                              identities[1]))
    # TODO: split transactions with multiple inputs into separate transactions
    # e.g. 10 to Bob, 8 to Alice in genesis block

    with open("ValidTransactionFile.json", "w") as f:
        for t in all_valid_transactions:
            f.write(t.JSON() + "\n$\n")

    return identities

if __name__ == "__main__":
    """
    Transaction Pools

    Format: {transaction number: TransactionBlock}
    """

    identities = main()
    UTP1 = readValidTransactionFile()
    UTP2 = readValidTransactionFile()
    UTP3 = readValidTransactionFile()
    UTP4 = readValidTransactionFile()
    UTP5 = readValidTransactionFile()
    dict_pairs = UTP1.items()
    pairs_iterator = iter(dict_pairs)
    genesis = next(pairs_iterator)
    VTP[genesis[0]] = genesis[1]
    print(VTP)
    print("----------------------------------------------------------------------")
    del UTP1[genesis[0]]
    del UTP2[genesis[0]]
    del UTP3[genesis[0]]
    del UTP4[genesis[0]]
    del UTP5[genesis[0]]
    testnode1 = Node(identities, UTP1, VTP, "Node1")
    testnode2 = Node(identities, UTP2, VTP, "Node2")
    testnode3 = Node(identities, UTP3, VTP, "Node3")
    testnode4 = Node(identities, UTP4, VTP, "Node4")
    testnode5 = Node(identities, UTP5, VTP, "Node5")
    testnode1.start()
    testnode2.start()
    testnode3.start()
    testnode4.start()
    testnode5.start()
    # testnode1.join()
    # testnode2.join()
    # testnode3.join()
    # testnode4.join()
    # testnode5.join()

