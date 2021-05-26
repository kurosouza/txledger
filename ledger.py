from pydantic import BaseModel
from typing import List, Dict
from datetime import date, datetime


class AccountNotFoundException(Exception):
    pass


class Transaction(BaseModel):
    """
    A transaction object
    
    Params:
    ======
    src_acct:   the source account to transfer from
    dst_acct:   the destination account to transfer to
    tx_date:    the transaction date
    tx_value:   the transaction value to transfer
    
    """

    src_acct: str
    dst_acct: str
    tx_date: datetime
    tx_value: float

    def __repr__(self):
        return "\tdate: {}\tfrom: {}\tto: {}\tamount:{}\n".format(self.tx_date, self.src_acct, self.dst_acct, self.tx_value)


class TransactionLog:
    """
    The transaction log: stores entire history of all transactions
    """

    accounts = {}
    transactions: List[Transaction] = []

    def __init__(self, transactions: List[Transaction] = None):
        if transactions is not None:
            """ Bulk load transactions:
                - create source accounts
                - create destination accounts
                - add transactions
            """
            [self.create_account(tx.src_acct) for tx in transactions if self.accounts.get(tx.src_acct) is None]
            [self.create_account(tx.dst_acct) for tx in transactions if self.accounts.get(tx.dst_acct) is None]
            [self.add_transaction(tx) for tx in transactions]

    def _rollforward(self, to_date: datetime = datetime.now(), account: str = None):
        tx_accounts = {}
        tx_log = []

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
                if account is not None and tx.dst_acct != account and tx.src_acct != account:
                    continue
                else:
                    tx_log.append(tx)
                    run_tx(tx)

        return tx_accounts, tx_log

    def create_account(self, name: str, balance: float = 0):
        """ Create a new account

        Params:
        ======
        name: account name
        balance: starting account balance
        """

        self.accounts[name] = balance

    def add_transaction(self, tx: Transaction):
        """ 
        Add a new transaction to the transaction log. This function also updates the global account state.
        
        Params:
        ======
        tx: Transaction(tx_date, src_acct, dst_acct, tx_value)
        """

        """ If accounts don't already exist, add them to the account registry """

        if self.accounts.get(tx.src_acct) is None:
            raise AccountNotFoundException("Could not find source account: {}".format(tx.src_acct))

        if self.accounts.get(tx.dst_acct) is None:
            raise AccountNotFoundException("Could not find desination account: {}".format(tx.dst_acct))

        """ append to transaction log """

        self.transactions.append(tx)

        """ update balances in global account registry """

        self.accounts[tx.src_acct] -= tx.tx_value
        self.accounts[tx.dst_acct] += tx.tx_value

    def get_account_balance(self, account_name: str) -> float:
        """ Get the balance for the specified account """
        if self.accounts.get(account_name) is None:
            raise AccountNotFoundException("This account '{}' does not exist.",format(account_name))
        return self.accounts[account_name]

    def get_account_balance_at(self, account_name: str, target_date_str: str) -> float:
        """ Get the balance for a given account at given date. This function works by replaying the transaction log
        to the specified date

        Params:
        ======
        account_name: account to check
        target_date: calculate balance up to specified date
        
        """
        target_date = datetime.strptime(target_date_str, "%Y-%m-%d %H:%M")
        replayed_log = self._rollforward(target_date)[0]
        if replayed_log.get(account_name) is None:
            raise AccountNotFoundException("Account name '{}' is invalid.".format(account_name))
        return replayed_log[account_name]


    def get_transactions(self, account: str = None) -> List[Transaction]:
        return list(filter(lambda tx: tx.src_acct == account or tx.dst_acct == account, self.transactions))


    def get_transactions_to_date(self, account: str, target_date_str: str) -> List[Transaction]:
        target_date = datetime.strptime(target_date_str, "%Y-%m-%d %H:%M")
        replayed_log = self._rollforward(target_date, account)
        return replayed_log[1]