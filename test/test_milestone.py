#test/test_milestone.py

from models.customer import Customer
from models.event_type import EventType
from models.milestone import Milestone
from models.user import User
from datetime import datetime

def test_create_milestone():
    customer = Customer(1, "Ana", "ana@mail.com", "1234")
    milestone = Milestone(1, EventType.TicketCreated, customer)
    assert milestone.id == 1
    assert milestone.event_type == EventType.TicketCreated
    assert milestone.user == customer
    assert milestone.created_at is not None


