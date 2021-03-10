from Crypto.PublicKey import RSA
from random import choice, randint
from transaction import Transaction


def generate_random_output(identities):
    #TODO: Generate output to two identities
    identity = choice(identities)
    value = randint(1,10)
    return {value: (hex(identity.n), hex(identity.e))}

def generate_valid_output(identity):
    return {5: (hex(identity.n), hex(identity.e))}


def generate_genesis_output(identities):
    identity = identities[0]
    value = 25
    return {value: (hex(identity.n), hex(identity.e))}

if __name__ == '__main__':
    #Generates 5 static identities to populate transaction file
    alice = RSA.generate(bits=1024)
    bob = RSA.generate(bits=1024)
    john = RSA.generate(bits=1024)
    max = RSA.generate(bits=1024)
    spencer = RSA.generate(bits=1024)
    identities = [alice, bob, john, max, spencer]

    #Genesis transaction
    transactions = [Transaction(None, generate_genesis_output(identities), identities[0])]

    #Set of 10 valid transactions
    #Alice has 25 coins
    all_valid_transactions = [Transaction(None, generate_genesis_output(identities), identities[0])]
    #Alice sends 5 coins to Bob
    all_valid_transactions.append(Transaction('trans',[all_valid_transactions[0].number, all_valid_transactions[0].output],
                                              generate_valid_output(identities[1]),
                                              identities[0]))
    #Bob sends 5 coins to John
    all_valid_transactions.append(Transaction('trans',[all_valid_transactions[1].number, all_valid_transactions[1].output],
                                              generate_valid_output(identities[2]),
                                              identities[1]))
    #John sends 5 coins to Max
    all_valid_transactions.append(Transaction('trans', [all_valid_transactions[2].number, all_valid_transactions[2].output],
                                              generate_valid_output(identities[3]),
                                              identities[2]))
    #max sends 5 coins to Spencer
    all_valid_transactions.append(Transaction('trans',[all_valid_transactions[3].number, all_valid_transactions[3].output],
                                              generate_valid_output(identities[4]),
                                              identities[3]))
    #Spencer sends 5 coins to Max
    all_valid_transactions.append(Transaction('trans',[all_valid_transactions[4].number, all_valid_transactions[4].output],
                                              generate_valid_output(identities[3]),
                                              identities[4]))
    #Max sends 5 coins to John
    all_valid_transactions.append(Transaction('trans',[all_valid_transactions[5].number, all_valid_transactions[5].output],
                                              generate_valid_output(identities[2]),
                                              identities[3]))
    #Spencer double spends 5 coins to Bob
    all_valid_transactions.append(Transaction('trans',[all_valid_transactions[4].number, all_valid_transactions[4].output],
                                              generate_valid_output(identities[1]),
                                              identities[4]))
    #Max receives 5 coins from Spencer, 5 coins from John
    all_valid_transactions.append(Transaction('merge',[[all_valid_transactions[3].number, all_valid_transactions[3].output],
                                                       [all_valid_transactions[5].number, all_valid_transactions[5].output]],
                                              {10 : (hex(identities[3].n), hex(identities[3].e))},
                                              identities[3]))
    #Alice sends 5 coins to Bob
    all_valid_transactions.append(Transaction([all_valid_transactions[8].number, all_valid_transactions[8].output],
                                              generate_valid_output(identities[1]),
                                              identities[0]))
    #Bob sends 5 coins to Max
    all_valid_transactions.append(Transaction([all_valid_transactions[9].number, all_valid_transactions[9].output],
                                              generate_valid_output(identities[3]),
                                              identities[1]))
    #TODO: split transactions with multiple inputs into separate transactions
    #e.g. 10 to Bob, 8 to Alice in genesis block
    for i in range(9):
        new_input = []
        for t in transactions:
            new_input.append(t.number)
        transaction = Transaction(new_input, generate_random_output(identities), choice(identities))
        transactions.append(transaction)

    # Write to file
    with open("TransactionFile.json", "w") as f:
        for t in transactions:
            f.write(t.JSON() + "\n$\n")
    with open("ValidTransactionFile.json", "w") as f:
        for t in all_valid_transactions:
            f.write(t.JSON() + "\n$\n")
