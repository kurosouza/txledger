from pydantic import BaseModel, Field
from typing import List
from datetime import date
from uuid import uuid4
from functools import reduce

class Transaction(BaseModel):
    src_acct: str
    dst_acct: str
    tx_date: date
    val: float

class Account(BaseModel):
    id: str = Field(default_factory = lambda: str(uuid4()))
    name: str
    balance: float

class InsufficientFundsException(Exception):
    pass

class NonExistentAccountException(Exception):
    pass

class TransactionLog:

    accounts: List[Account] = []
    transactions: List[Transaction] = []

    def __init__(self):
        pass

    def create_account(self, name: str, balance: float = 0):
        account = Account(name = name, balance = balance)
        self.accounts.append(account)

    def add_transaction(self, src_acct, dst_acct, tx_date, tx_value):
        """ 
        Add a new transaction 
        
        Params:

        src_acct:   the source account to transfer from
        dst_acct:   the destination account to transfer to
        tx_date:    the transaction date
        tx_value:   the transaction value to transfer
        """
        
        tx = Transaction(src_acct = src_acct, dst_acct = dst_acct, tx_date = tx_date, tx_value = tx_value)
        
        if len(filter(lambda account: account.src_acct == src_acct, self.accounts)) == 0:
            raise NonExistentAccountException("The source account does not exist")

        if len(filter(lambda account: account.dst_acct == dst_acct, self.accounts)) == 0:
            raise NonExistentAccountException("The destination account does not exist")

        self.transactions.append(tx)

    def get_account_balance(self, account_name) -> float:
        """ Get the balance for the specified account """

    def get_account_balance_at(self, account_name, target_date: date) -> float:
        """ Get the balance for a given account at given date """