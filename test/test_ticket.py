from models.ticket import Ticket
from models.ticket_status import TicketStatus
import pytest

def test_crear_ticket():
    ticket = Ticket(1, "heladera rota", "heladera no enfria")
    assert ticket.id == 1
    assert ticket.title == "heladera rota"
    assert ticket.description == "heladera no enfria"
    assert ticket.status == TicketStatus.Open
    assert ticket.created_at is not None
    assert ticket.closed_at is None
    assert ticket.category is None
    assert ticket.priority is None
    assert ticket.product is None
    

def test_close_ticket():
    ticket = Ticket(1, "heladera rota", "heladera no enfria")
    ticket.close()
    assert ticket.status == TicketStatus.Closed


def test_reopen_ticket():
    ticket = Ticket(1, "heladera rota", "heladera no enfria")
    ticket.close()
    ticket.reopen()
    assert ticket.status == TicketStatus.Open

def test_reopen_open_ticket():
    ticket = Ticket(1, "heladera rota", "heladera no enfria")
    with pytest.raises(Exception):
        ticket.reopen()