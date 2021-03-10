import json
from time import sleep
from transactionblock import TransactionBlock


FILE = "TransactionFile.json"


def readTransactionFile():
    """
    Returns a list where each element is a dictionary representation of a transaction
    in the Transaction File
    """
    utp = {}

    with open(FILE, "r") as f:
        transactions = [json.loads(t) for t in f.read()[:-2].split("$")]

    for t in transactions:
        trans = TransactionBlock(t["type"],
                                 t["input"],
                                 t["output"],
                                 t["signature"],
                                 t["number"])
        utp[trans.number] = trans

    return utp


if __name__ == "__main__":
    """
    Transaction Pools

    Format: {transaction number: TransactionBlock}
    """
    UTP = readTransactionFile()
    print(UTP)
    VTP = {}

