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


    def _rollforward(self, to_date: datetime = datetime.now()):
        tx_accounts = {}

        def run_tx(tx):
            """ Reduce function: update account balances with transaction values for tx1 and tx2 """
            print("run_tx #1 - {0}".format(tx))
            
            if tx_accounts.get(tx.src_acct) is None:
                tx_accounts[tx.src_acct] = 0

            if tx_accounts.get(tx.dst_acct) is None:
                tx_accounts[tx.dst_acct] = 0

            tx_accounts[tx.src_acct] -= tx.tx_value
            tx_accounts[tx.dst_acct] += tx.tx_value

        # reduce(run_tx, self.transactions)
        for tx in self.transactions:
            if tx.tx_date < to_date:
                run_tx(tx) 

        return tx_accounts


    def create_account(self, name: str, balance: float = 0):        
        """ Create a new account

        Params:
        ======
        name: account name
        balance: starting account balance
        """

        self.accounts[name] = balance


    def add_transaction(self, src_acct, dst_acct, tx_date, tx_value):
        """ 
        Add a new transaction to the transaction log. This function also updates the global account state.
        
        Params:
        ======
        src_acct:   the source account to transfer from
        dst_acct:   the destination account to transfer to
        tx_date:    the transaction date
        tx_value:   the transaction value to transfer
        """

        tx = Transaction(src_acct = src_acct, dst_acct = dst_acct, tx_date = tx_date, tx_value = tx_value)
        
        """ If accounts don't already exist, add them to the account registry """

        if self.accounts.get(src_acct) is None:
            self.accounts[src_acct] = 0

        if self.accounts.get(dst_acct) is None:
            self.accounts[dst_acct] = 0

        """ append to transaction log """

        self.transactions.append(tx)

        """ update balances in global account registry """

        self.accounts[tx.src_acct] -= tx.tx_value
        self.accounts[tx.dst_acct] += tx.tx_value


    def get_account_balance(self, account_name) -> float:
        """ Get the balance for the specified account """
        return self.accounts[account_name]

    def get_account_balance_at(self, account_name, target_date: datetime) -> float:
        """ Get the balance for a given account at given date. This function works by replaying the transaction log
        to the specified date

        Params:
        ======
        account_name: account to check
        target_date: calculate balance up to specified date
        
        """
        return self._rollforward(target_date)[account_name]