# txledger - Transaction Ledger demo application

This application demonstrates the use of a transaction ledger to keep a record of transactions occuring between multiple accounts.

## Setup

To test the application, first install the application dependencies:

```
pip install pydantic
```

Then run the python main application

```
python cli.py
```

You can run the tests by running pytest from the project base directory:

```
pytest
```

The CLI app imports an existing list of transactions from the transactions.csv file. You can update this file to save a custom list of transactions


## API

To create a new ledger, initialize a new ledger instance:

```python
from ledger import TransactionLog, Transaction

ledger = TransactionLog()

```

or from an existing list of transactions

```python
tx_data = {
    'tx_date': '2021-5-20 11:00',
    'src_acct': 'john',
    'dst_acct': 'sarah',
    'tx_value': 500
}

transaction = Transaction(**tx_data)

ledger = TransactionLog(transactions = [transaction])
```

or you can load transactions from a csv file:

```python
import filereader

transactions = filereader.load_from_file('transactions.csv')
transaction_log = TransactionLog(transactions)

```

Next, create accounts for anyone you want to participate in transactions

```python
ledger.create_account('paul')
ledger.create_account('coffee shop')
```

You can now create a transaction

```python
tx = Transaction(tx_date = '2021-5-13 09:00', src_acct='paul', dst_acct='coffee shop', tx_value = 12.)
ledger.add_transaction(tx)
```

retrieve the balance for a specific account by calling TransactionLog.get_account_balance(account_name):

```python
print("John's account balance: ", ledger.get_account_balance('paul'))
print("Coffee shop account balance: ", ledger.get_account_balance('paul'))
```

You can retrieve the account balance for an account at a given date by calling *TransactionLog.get_account_balance_at(account_name, target_date)*

```python
    ledger = TransactionLog()

    # create accounts
    ledger.create_account('john')
    ledger.create_account('james')

    # add some transactions
    transaction_log.add_transaction(Transaction(src_acct='john', dst_acct='james', tx_date = '2021-1-1 08:00 tx_value = 100))
    transaction_log.add_transaction(Transaction(src_acct='john', dst_acct='james', tx_date = '2021-2-10 08:00', tx_value = 100))
    transaction_log.add_transaction(Transaction(src_acct='john', dst_acct='james', tx_date = '2021-3-10 08:00', tx_value = 100))

    # get balance for accounts at 2020-2-25, this should be 200.0
    transaction_log.get_account_balance_at('james', '2021-2-25 12:00')
```