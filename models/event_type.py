from enum import Enum

class EventType(Enum) :
    TicketCreated = "Ticket Creado"
    TicketAssigned = "Ticket Asignado"
    StatusUpdated = "Estado Actualizado"
    TicketClosed = "Ticket Cerrado"
    TicketReopened = "Ticket Reabierto"
    TicketUpdated = "Ticket Actualizado"
