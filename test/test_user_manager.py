from managers.user_manager import UserManager
from test.fake_repository import FakeRepository
import pytest 

def test_create_customer():
    manager = UserManager(FakeRepository())
    customer = manager.create_customer("Ana", "ana@mail.com", "1234")
    assert customer in manager.list_customers()
    assert customer.name == "Ana"
    assert customer.email == "ana@mail.com"


def test_create_duplicate_customer():
    manager = UserManager(FakeRepository())
    customer = manager.create_customer("Ana", "ana@mail.com", "1234")
    with pytest.raises(Exception):
        manager.create_customer("Ana", "ana@mail.com", "1234")