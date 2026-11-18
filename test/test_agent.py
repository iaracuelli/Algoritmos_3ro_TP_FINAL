from models.agent import Agent
from models.ticket import Ticket
import pytest

def test_create_agent():
    agent = Agent(1, "German", "agenteGerman@gmail.com", "1234")
    assert agent.id == 1
    assert agent.name == "German"
    assert agent.email ==  "agenteGerman@gmail.com"
    assert agent.password == "1234"
    assert agent.active == True

def test_take_ticket_active():
    agent = Agent (1, "German", "agenteGerman@gmail.com", "1234")
    ticket = Ticket(1, "heladera rota", "heladera no enfria")
    agent.take_ticket(ticket)
    assert ticket in agent.tickets

def test_take_ticket_inactive():
    agent = Agent (1, "German", "agenteGerman@gmail.com", "1234")
    ticket = Ticket(1, "heladera rota", "heladera no enfria")
    agent.active = False
    with pytest.raises(Exception):
        agent.take_ticket(ticket)