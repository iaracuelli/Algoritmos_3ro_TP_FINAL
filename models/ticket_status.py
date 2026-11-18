from enum import Enum

class TicketStatus(Enum) :
    Open = "Abierto"
    InProgress = "En Progreso"
    Closed = "Cerrado"
    Resolved = "Resuelto"