from Crypto.PublicKey import RSA
from random import choice, randint
from transaction import Transaction


def generate_random_output(identities):
    identity = choice(identities)
    value = randint(1,10)
    return {value: (hex(identity.n), hex(identity.e))}

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
    for i in range(9):
        new_input = []
        for t in transactions:
            new_input.append(t.number)
        transaction = Transaction(new_input, generate_random_output(identities), choice(identities))
        transactions.append(transaction)

    test = ""
    for t in transactions:
        test += t.JSON()
        test += '\n$\n'
    print(test)
