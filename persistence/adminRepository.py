# persistence/admin_repository.py
# Contrato para persistencia de admin
#No tiene implementación concreta.
# Permite desacoplar la lógica de negocio de la base de datos.

from abc import ABC, abstractmethod

class AdminRepository(ABC):

    @abstractmethod
    def save(self, admin):
        """
        Guarda un admin en la fuente de datos.
        Devuelve el admin con su ID asignado.
        """
        pass

    @abstractmethod
    def list(self):
        """
        Devuelve una lista de todos los admin.
        """
        pass

    @abstractmethod
    def get_by_id(self, id):
        """
        Devuelve un admin según su ID o None si no existe.
        """
        pass


#Es una interfaz (contrato) que define qué operaciones se pueden hacer con admin, pero no cómo se hacen.
#El repositorio define el contrato de persistencia, desacoplando la lógica de negocio del mecanismo de almacenamiento.

#DIP: el gestor depende de una abstracción
#Open/Closed: puedo agregar otro repositorio sin modificar gestores
#Low Coupling: la BD queda aislada