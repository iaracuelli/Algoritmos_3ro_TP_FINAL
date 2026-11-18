# persistence/customer_repository.py
# Contrato para persistencia de clientes
#No tiene implementación concreta.
# Permite desacoplar la lógica de negocio de la base de datos.

from abc import ABC, abstractmethod

class CustomerRepository(ABC):

    @abstractmethod
    def save(self, customer):
        """
        Guarda un cliente en la fuente de datos.
        Devuelve el cliente con su ID asignado.
        """
        pass

    @abstractmethod
    def list(self):
        """
        Devuelve una lista de todos los clientes.
        """
        pass

    @abstractmethod
    def get_by_id(self, id):
        """
        Devuelve un cliente según su ID o None si no existe.
        """
        pass

    @abstractmethod
    def update(self, item):
        """
        Actualiza en la fuente de datos un cliente que ya existe.
        """
        pass


#Es una interfaz (contrato) que define qué operaciones se pueden hacer con clientes, pero no cómo se hacen.
#El repositorio define el contrato de persistencia, desacoplando la lógica de negocio del mecanismo de almacenamiento.

#DIP: el gestor depende de una abstracción
#Open/Closed: puedo agregar otro repositorio sin modificar gestores
#Low Coupling: la BD queda aislada