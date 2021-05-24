import os
from filereader import load_from_file
from ledger import Transaction, TransactionLog

if __name__ == '__main__':
    transactions = load_from_file('transactions.csv')
    tx_log = TransactionLog(transactions=transactions)
    print('James: {}'.format(tx_log.get_account_balance('james')))
    print('John: {}'.format(tx_log.get_account_balance('john')))
    print('done.')