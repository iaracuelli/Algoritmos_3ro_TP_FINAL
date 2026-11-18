from managers.ticket_manager import TicketManager
from test.fake_repository import FakeRepository
import pytest

def test_create_ticket():
    manager = TicketManager(FakeRepository())
    ticket = manager.create_ticket("heladera rota", "heladera no enfria")
    assert ticket in manager.list_tickets()
    assert ticket.id == 1
    assert ticket.title == "heladera rota"
    assert ticket.description == "heladera no enfria"


def test_list_ticket():
    manager = TicketManager(FakeRepository())
    manager.create_ticket("heladera rota", "heladera no enfria")
    manager.create_ticket("lavarropas roto", "no centrifuga")
    tickets = manager.list_tickets()
    assert len(tickets) == 2


def test_get_ticket_by_id():
    manager = TicketManager(FakeRepository())
    manager.create_ticket("heladera rota", "heladera no enfria")
    ticket = manager.get_ticket_by_id(1)
    assert ticket.id == 1
    assert ticket.title == "heladera rota"
