from models.ticket_status import TicketStatus
from models.event_type import EventType
from models.milestone import Milestone
from datetime import datetime


def same_user(user1, user2):
    # Dos usuarios son el mismo si son del mismo tipo (Customer, Agent, Admin) y tienen el mismo id
    return type(user1) is type(user2) and user1.id == user2.id


class Ticket:
        def __init__(self, id, title, description, 
                     status=TicketStatus.Open, 
                     created_at=None):   # id puede ser None al crearse y luego lo asigna la base de datos
                self.id = id
                self.title = title                
                self.description = description    
                self.status = status
                self.created_at = created_at if created_at else datetime.now()
                self.closed_at = None
                self.category = None
                self.priority = None
                self.product = None
                self.customer = None        # cliente que creo el ticket
                self.agent = None           # agente que lo atiende
                self.milestones = []        # composicion: los hitos pertenecen al ticket
                self.messages = []          # composicion: los mensajes pertenecen al ticket

        def open(self):
            self.status = TicketStatus.Open
            self.closed_at = None

        def close(self, user=None):
            self.status = TicketStatus.Closed
            self.closed_at = datetime.now()
            if user is not None:
                self.add_milestone(EventType.TicketClosed, user)

        def reopen(self, user=None):
               if self.status == TicketStatus.Closed:
                self.open()
                if user is not None:
                    self.add_milestone(EventType.TicketReopened, user)
               else:
                     raise Exception("El ticket no esta cerrado")

        def updateStatus(self, status, user=None):
            if status == TicketStatus.Closed:
                self.close(user)
                return
            self.status = status
            self.closed_at = None
            if user is not None:
                self.add_milestone(EventType.StatusUpdated, user)

        def updateInfo(self, category, priority, user=None):
            # cambia categoria y/o prioridad; devuelve True si hubo algun cambio
            changed = False
            if category is not None and category != self.category:
                self.category = category
                changed = True
            if priority is not None and priority != self.priority:
                self.priority = priority
                changed = True
            if changed and user is not None:
                self.add_milestone(EventType.TicketUpdated, user)
            return changed

        def assign_to(self, agent, user):
            self.agent = agent
            self.add_milestone(EventType.TicketAssigned, user)

        def add_milestone(self, event_type, user):
            milestone = Milestone(None, event_type, user)
            self.milestones.append(milestone)
            return milestone

        def add_message(self, message):
            self.messages.append(message)
            return message

        def getMilestones(self):
            return self.milestones

        def getMessages(self):
            return self.messages

        def unread_count(self, user):
            # mensajes sin leer que NO escribio el usuario (los que le llegaron a el)
            return len([m for m in self.messages if not m.read and not same_user(m.sender, user)])

        def mark_messages_read(self, user):
            for message in self.messages:
                if not same_user(message.sender, user):
                    message.read = True
