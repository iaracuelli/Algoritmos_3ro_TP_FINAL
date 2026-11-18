#models/message.py
from models.user import User
from datetime import datetime


class Message():
    def __init__(self, id, content, sender,  read=False, created_at=None):
        self.id = id
        self.content = content
        self.sender = sender
        self.read = read
        self.created_at = created_at if created_at else datetime.now()