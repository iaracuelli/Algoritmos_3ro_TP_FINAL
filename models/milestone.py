#models/milestone.py
from models.event_type import EventType
from models.user import User
from datetime import datetime


class Milestone():
    def __init__(self, id, event_type, user, created_at=None):
        self.id = id
        self.event_type = event_type
        self.user = user
        self.created_at = created_at if created_at else datetime.now()