#models/agent.py
from models.user import User
from models.ticket import Ticket
from models.ticket_status import TicketStatus
from models.message import Message

class Agent(User):
        def __init__(self, id, name, email, password):  
                super().__init__(id, name, email, password)     # llamo a User.__init__
                self.active = True                              # atributo de agent
                self.tickets = []  # lista de tickets asignados  un agent puede tomar mas de un ticket y se guardar en una lista


        def take_ticket(self, ticket):
                if self.active == True:
                    self.tickets.append(ticket) 
                    ticket.assign_to(self, self)
                else:
                    raise Exception("Agente no activo")

        def viewAssignedTickets(self):
                # tickets asignados que todavia no se cerraron
                return [t for t in self.tickets if t.status != TicketStatus.Closed]

        def listTickets(self):
                return self.tickets

        def viewDetailTicket(self, ticket):
                ticket.mark_messages_read(self)                 # al abrir el ticket se leen los mensajes del cliente
                return ticket

        def respondTicket(self, ticket, content):
                if ticket.status == TicketStatus.Closed:
                    raise Exception("El ticket está cerrado")
                message = Message(None, content, self)
                ticket.add_message(message)
                if ticket.status == TicketStatus.Open:          # al responder, el ticket pasa a En Progreso
                    ticket.updateStatus(TicketStatus.InProgress, self)
                return message

        def updateStatus(self, ticket, status):
                ticket.updateStatus(status, self)

        def closeTicket(self, ticket):
                ticket.close(self)

        def viewHistoryTicket(self, ticket):
                return ticket.getMilestones()
