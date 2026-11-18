#pytest test/test_ticket.py -v

# models/user.py

from abc import ABC

class User(ABC):
    def __init__(self, id, name, email, password):
        self.id = id
        self.name = name
        self.email = email
        self.password = password

    def login(self, password) -> bool:
        return self.password == password

    def logout(self):
        pass