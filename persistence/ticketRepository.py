# persistence/ticket_repository.py
# Contrato para persistencia de tickets
#No tiene implementación concreta.
# Permite desacoplar la lógica de negocio de la base de datos.

from abc import ABC, abstractmethod

class TicketRepository(ABC):

    @abstractmethod
    def save(self, ticket):
        """
        Guarda un ticket en la fuente de datos.
        Devuelve el ticket con su ID asignado.
        """
        pass

    @abstractmethod
    def list(self):
        """
        Devuelve una lista de todos los ticket.
        """
        pass

    @abstractmethod
    def get_by_id(self, id):
        """
        Devuelve un ticket según su ID o None si no existe.
        """
        pass

    @abstractmethod
    def update(self, item):
        """
        Actualiza en la fuente de datos un ticket que ya existe.
        """
        pass


#Es una interfaz (contrato) que define qué operaciones se pueden hacer con tickets, pero no cómo se hacen.
#El repositorio define el contrato de persistencia, desacoplando la lógica de negocio del mecanismo de almacenamiento.

#DIP: el gestor depende de una abstracción
#Open/Closed: puedo agregar otro repositorio sin modificar gestores
#Low Coupling: la BD queda aislada