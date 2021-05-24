from pydantic import BaseModel
from typing import List

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