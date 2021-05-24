from pydantic import BaseModel
from typing import List, Dict
from datetime import date, datetime

class AccountNotFoundException(Exception):
    pass

class Transaction(BaseModel):
    src_acct: str
    dst_acct: str
    tx_date: datetime
    tx_value: float


class TransactionLog:

    accounts = {}
    transactions: List[Transaction] = []

    def __init__(self, transactions: List[Transaction] = None):
        if transactions is not None:
            [self.add_transaction(tx) for tx in transactions]


    def _rollforward(self, to_date: datetime = datetime.now()):
        tx_accounts = {}

        def run_tx(tx):
            """ Execute transactions using local account dictionary """
            print("run_tx #1 - {0}".format(tx))
            
            if tx_accounts.get(tx.src_acct) is None:
                tx_accounts[tx.src_acct] = 0

            if tx_accounts.get(tx.dst_acct) is None:
                tx_accounts[tx.dst_acct] = 0

            tx_accounts[tx.src_acct] -= tx.tx_value
            tx_accounts[tx.dst_acct] += tx.tx_value


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
            raise AccountNotFoundException("Could not find source account: {}".format(src_acct))

        if self.accounts.get(dst_acct) is None:
            raise AccountNotFoundException("Could not find desination account: {}".format(dst_acct))

        """ append to transaction log """

        self.transactions.append(tx)

        """ update balances in global account registry """

        self.accounts[tx.src_acct] -= tx.tx_value
        self.accounts[tx.dst_acct] += tx.tx_value


    def get_account_balance(self, account_name) -> float:
        """ Get the balance for the specified account """
        return self.accounts[account_name]

    def get_account_balance_at(self, account_name, target_date_str: str) -> float:
        """ Get the balance for a given account at given date. This function works by replaying the transaction log
        to the specified date

        Params:
        ======
        account_name: account to check
        target_date: calculate balance up to specified date
        
        """
        target_date = datetime.strptime(target_date_str, "%Y-%m-%d %H:%M")
        return self._rollforward(target_date)[account_name]