import json
from transactionblock import TransactionBlock

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


UTP = readValidTransactionFile()
VTP = {}
