#test/test_message.py

from models.message import Message
from models.customer import Customer
from models.user import User
from datetime import datetime

def test_create_message():
    customer = Customer(1, "Ana", "ana@mail.com", "1234")
    message = Message(1, "hola", customer)
    assert message.id == 1
    assert message.content == "hola"
    assert message.sender == customer
    assert message.read == False
    assert message.created_at is not None


