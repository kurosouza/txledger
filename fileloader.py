import csv
import datetime
from ledger import Transaction, TransactionLog


def load_from_file(filename: str):
    transactions = []
    with open(filename, 'r') as file:
        csvreader = csv.reader(file, delimiter=',')
        for row in csvreader:
            tx = Transaction(tx_date = row[0], src_acct = row[1], dst_acct= row[2], tx_value = row[3])
            transactions.append(tx)
    return transactions


def save_to_file(filename: str, transaction_log: TransactionLog):
    with open(filename, 'w', newline='\n') as file:
        writer = csv.writer(file, delimiter=',')
        for tx in transaction_log.transactions:
            writer.writerow([datetime.datetime.strftime(tx.tx_date, "%Y-%m-%d %H:%M"), tx.src_acct, tx.dst_acct, tx.tx_value])