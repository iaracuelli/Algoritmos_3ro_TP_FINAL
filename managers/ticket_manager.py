from models.ticket import Ticket
from models.ticket_status import TicketStatus
from models.event_type import EventType
from datetime import datetime

class TicketManager:
    def __init__(self, repository):
        self.repository = repository    


    def create_ticket(self, title, description, status=TicketStatus.Open, created_at=None,
                      customer=None, product=None, category=None, priority=None):
        ticket = Ticket(
            id=None,
            title=title,
            description=description,
            status = status,
            created_at = created_at
            
        )
        ticket.customer = customer
        ticket.product = product
        ticket.category = category
        ticket.priority = priority
        if customer is not None:
            ticket.add_milestone(EventType.TicketCreated, customer)
        return self.repository.save(ticket)

    def list_tickets(self):
        return self.repository.list()
    

    def get_ticket_by_id(self, id):
        return self.repository.get_by_id(id)

    def update_ticket(self, ticket):
        return self.repository.update(ticket)
