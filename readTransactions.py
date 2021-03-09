import json


FILE = "TransactionFile.json"


def readTransactionFile():
    """
    Returns a list where each element is a dictionary representation of a transaction
    in the Transaction File
    """

    with open(FILE, "r") as f:
        transactions = [json.loads(t) for t in f.read()[:-2].split("$")]

    return transactions
