import csv
from ledger import Transaction


def load_from_file(filename: str):
    transactions = []
    with open(filename, 'r') as file:
        csvreader = csv.reader(file, delimiter=',')
        for row in csvreader:
            tx = Transaction(tx_date = row[0], src_acct = row[1], dst_acct= row[2], tx_value = row[3])
            transactions.append(tx)

    return transactions