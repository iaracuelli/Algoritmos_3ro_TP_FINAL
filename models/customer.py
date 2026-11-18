#models/customer.py
from models.user import User
from models.message import Message
from models.ticket_status import TicketStatus

class Customer(User):
        def __init__(self, id, name, email, password):  
                super().__init__(id, name, email, password)     # llamo a User.__init__
                self.active = True                              # atributo de Customer
                self.tickets = []                               # tickets del cliente (Customer 1 - * Ticket)

        def listTickets(self):
                return self.tickets

        def viewDetailTicket(self, ticket):
                ticket.mark_messages_read(self)                 # al abrir el ticket se leen los mensajes del agente
                return ticket

        def sendMessage(self, ticket, content):
                if ticket.status == TicketStatus.Closed:
                    raise Exception("El ticket está cerrado")
                message = Message(None, content, self)
                ticket.add_message(message)
                return message

        def closeTicket(self, ticket):
                ticket.close(self)

        def reopenTicket(self, ticket):
                ticket.reopen(self)
