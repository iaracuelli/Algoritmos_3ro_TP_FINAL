from models.admin import Admin
from models.ticket import Ticket
from models.agent import Agent


def test_create_admin():
    admin = Admin(1, "Admin", "admin@mail.com", "1234")
    assert admin.id == 1
    assert admin.name == "Admin"
    assert admin.email == "admin@mail.com"
    assert admin.password == "1234"


def test_assign_ticket():
    admin = Admin(1, "Admin", "admin@mail.com", "1234")
    ticket = Ticket(1, "heladera rota", "heladera no enfria")
    agent = Agent (1, "German", "agenteGerman@gmail.com", "1234")
    admin.assignTicket(agent, ticket)
    assert ticket in agent.tickets


def test_reassign_ticket():
    admin = Admin(1, "Admin", "admin@mail.com", "1234")
    ticket = Ticket(1, "heladera rota", "heladera no enfria")
    agent1 = Agent (1, "German", "agenteGerman@gmail.com", "1234")
    agent2 = Agent (2, "Alfredo", "agenteAlfredo@gmail.com", "1234")
    admin.assignTicket(agent1, ticket)
    
    admin.reassignTicket(agent1, agent2, ticket)

    assert ticket in agent2.tickets
    assert ticket not in agent1.tickets