from pydantic import BaseModel
from typing import List
import pytest
from ledger import TransactionLog, Transaction, AccountNotFoundException

class User(BaseModel):
        name: str
        age: int

class UserStore(BaseModel):
    users: List[User] = []


def test_user_model():
    user1 = User(name = "John Snow", age = 25)

    assert user1.age == 25
    assert user1.name == "John Snow"


def test_user_list():
    user_store = UserStore()
    
    assert len(user_store.users) == 0


def test_create_account_with_500_balance():
    transaction_log = TransactionLog()
    transaction_log.create_account('john wick', 500.)

    assert transaction_log.get_account_balance('john wick') == 500.


def test_create_account_with_zero_balance():
    transaction_log = TransactionLog()
    transaction_log.create_account('james wick')

    assert transaction_log.get_account_balance('james wick') == 0.

def test_add_transaction():
    transaction_log = TransactionLog()
    transaction_log.create_account('john')
    transaction_log.create_account('james')
    tx = Transaction(tx_date = '2021-5-24 11:00', src_acct = 'john', dst_acct = 'james', tx_value = 100.)
    transaction_log.add_transaction(tx)

    assert transaction_log.get_account_balance('james') == 100
    assert transaction_log.get_account_balance('john') == -100


def test_get_balance_at_date():
    transaction_log = TransactionLog()
    transaction_log.create_account('john')
    transaction_log.create_account('james')

    transaction_log.add_transaction(Transaction(src_acct='john', dst_acct='james', tx_date = '2021-1-10 08:00', tx_value = 100))
    transaction_log.add_transaction(Transaction(src_acct='john', dst_acct='james', tx_date = '2021-2-10 08:00', tx_value = 100))
    transaction_log.add_transaction(Transaction(src_acct='john', dst_acct='james', tx_date = '2021-3-10 08:00', tx_value = 100))

    assert transaction_log.get_account_balance_at('james', '2021-2-25 12:00') == 200.


def test_invalid_account_raises_account_not_found():
    transaction_log = TransactionLog()
    with pytest.raises(AccountNotFoundException):
        transaction_log.get_account_balance('hendrix')


def test_get_transactions_for_account():
    tx1 = Transaction(src_acct='john', dst_acct='james', tx_date = '2021-1-10 08:00', tx_value = 100)
    tx2 = Transaction(src_acct='peter', dst_acct='sarah', tx_date = '2021-2-10 08:00', tx_value = 50)
    transaction_log = TransactionLog([tx1, tx2])
    
    assert transaction_log.get_transactions('peter') == [tx2]


def test_get_transactions_for_account_to_date():
    tx1 = Transaction(src_acct='john', dst_acct='james', tx_date = '2021-1-1 08:00', tx_value = 50)
    tx2 = Transaction(src_acct='peter', dst_acct='sarah', tx_date = '2021-1-2 08:00', tx_value = 50)
    tx3 = Transaction(src_acct='john', dst_acct='james', tx_date = '2021-1-3 08:00', tx_value = 50)
    tx4 = Transaction(src_acct='peter', dst_acct='sarah', tx_date = '2021-1-4 08:00', tx_value = 50)
    transaction_log = TransactionLog([tx1, tx2, tx3, tx4])

    assert transaction_log.get_transactions_to_date('james', '2021-1-2 23:00') == [tx1]