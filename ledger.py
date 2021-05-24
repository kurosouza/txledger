from pydantic import BaseModel, Field
from typing import List, Dict
from datetime import date, datetime
from uuid import uuid4
from functools import reduce

class Transaction(BaseModel):
    src_acct: str
    dst_acct: str
    tx_date: datetime
    tx_value: float

class Account(BaseModel):
    id: str = Field(default_factory = lambda: str(uuid4()))
    name: str
    balance: float

class NonExistentAccountException(Exception):
    pass

class TransactionLog:

    accounts = {}
    transactions: List[Transaction] = []

    def __init__(self, transactions = None):
        if transactions is not None:
            [self.transactions.append(tx) for tx in transactions]


    def _rollforward(self):
        
        def run_tx(tx1, tx2):
            """ Reduce function: update account balances with transaction values for tx1 and tx2 """
            print(f'tx #1 - {0}, tx #2 - {1}', tx1, tx2)
            
            self.accounts[tx1.src_acct] -= tx1.tx_value
            self.accounts[tx1.dst_acct] += tx1.tx_value

            self.accounts[tx2.src_acct] -= tx2.tx_value
            self.account[tx2.dst_acct] += tx2.tx_value
            

        reduce(run_tx, self.transactions)


    def create_account(self, name: str, balance: float = 0):        
        self.accounts[name] = balance


    def add_transaction(self, src_acct, dst_acct, tx_date, tx_value):
        """ 
        Add a new transaction 
        
        Params:

        src_acct:   the source account to transfer from
        dst_acct:   the destination account to transfer to
        tx_date:    the transaction date
        tx_value:   the transaction value to transfer
        """

        tx_info = {
            'src_acct': src_acct,
            'dst_acct': dst_acct,
            'tx_date': tx_date,
            'tx_value': tx_value
        }

        tx = Transaction(src_acct = src_acct, dst_acct = dst_acct, tx_date = tx_date, tx_value = tx_value)
        
        if self.accounts.get(src_acct) is None:
            raise NonExistentAccountException("The source account does not exist")

        if self.accounts.get(dst_acct) is None:
            raise NonExistentAccountException("The destination account does not exist")

        self.transactions.append(tx)
        self._rollforward()

    def get_account_balance(self, account_name) -> float:
        """ Get the balance for the specified account """
        return self.accounts[account_name]

    def get_account_balance_at(self, account_name, target_date: date) -> float:
        """ Get the balance for a given account at given date """