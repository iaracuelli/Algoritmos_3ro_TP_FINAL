# persistence/ticket_repositoryDB.py
# Implementación concreta del repositorio de ticket usando SQLite.
# Esta clase cumple el contrato TicketRepository.
# Guarda el ticket y, como forman parte de él (composición), sus hitos y mensajes.

import sqlite3
from datetime import datetime
from models.ticket import Ticket
from models.ticket_status import TicketStatus
from models.ticket_category import TicketCategory
from models.ticket_priority import TicketPriority
from models.event_type import EventType
from models.milestone import Milestone
from models.message import Message
from models.customer import Customer
from models.agent import Agent
from models.admin import Admin


class TicketRepositoryDB:
    # Para reconstruir cliente, agente, producto y usuarios de hitos/mensajes
    # recibe los repositorios correspondientes (si no se pasan, quedan en None).
    def __init__(self, db_path="tickets.db", customer_repo=None, agent_repo=None,
                 admin_repo=None, product_repo=None):
        self.conn = sqlite3.connect(db_path)
        self.customer_repo = customer_repo
        self.agent_repo = agent_repo
        self.admin_repo = admin_repo
        self.product_repo = product_repo
        self._create_tables()                            

    def _create_tables(self):                              
        cursor = self.conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS tickets (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                description TEXT NOT NULL,
                status TEXT NOT NULL,
                created_at TEXT NOT NULL,
                closed_at TEXT,
                category TEXT,
                priority TEXT,
                customer_id INTEGER,
                agent_id INTEGER,
                product_id INTEGER
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS milestones (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                ticket_id INTEGER NOT NULL,
                event_type TEXT NOT NULL,
                user_id INTEGER,
                user_role TEXT,
                created_at TEXT NOT NULL
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                ticket_id INTEGER NOT NULL,
                content TEXT NOT NULL,
                sender_id INTEGER,
                sender_role TEXT,
                read INTEGER NOT NULL DEFAULT 0,
                created_at TEXT NOT NULL
            )
        """)
        self.conn.commit()

    # ---------- conversiones auxiliares ----------

    def _role(self, user):
        if isinstance(user, Customer):
            return "customer"
        if isinstance(user, Agent):
            return "agent"
        if isinstance(user, Admin):
            return "admin"
        return None

    def _user(self, role, id):
        repos = {"customer": self.customer_repo, "agent": self.agent_repo, "admin": self.admin_repo}
        repo = repos.get(role)
        if repo is None or id is None:
            return None
        return repo.get_by_id(id)

    def _date(self, text):
        return datetime.fromisoformat(text) if text else None

    # ---------- guardar ----------

    def _ticket_values(self, ticket):
        return (
            ticket.title,
            ticket.description,
            ticket.status.name,
            ticket.created_at.isoformat(),
            ticket.closed_at.isoformat() if ticket.closed_at else None,
            ticket.category.name if ticket.category else None,
            ticket.priority.name if ticket.priority else None,
            ticket.customer.id if ticket.customer else None,
            ticket.agent.id if ticket.agent else None,
            ticket.product.id if ticket.product else None,
        )

    def save(self, ticket):                    
        cursor = self.conn.cursor()
        cursor.execute(
            """INSERT INTO tickets (title, description, status, created_at, closed_at,
               category, priority, customer_id, agent_id, product_id)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            self._ticket_values(ticket)
        )
        ticket.id = cursor.lastrowid               
        self._save_children(ticket)
        self.conn.commit()
        return ticket

    def update(self, ticket):
        cursor = self.conn.cursor()
        cursor.execute(
            """UPDATE tickets SET title = ?, description = ?, status = ?, created_at = ?,
               closed_at = ?, category = ?, priority = ?, customer_id = ?, agent_id = ?,
               product_id = ? WHERE id = ?""",
            self._ticket_values(ticket) + (ticket.id,)
        )
        self._save_children(ticket)
        self.conn.commit()
        return ticket

    def _save_children(self, ticket):
        cursor = self.conn.cursor()
        for milestone in ticket.milestones:
            if milestone.id is None:                    # solo se insertan los nuevos
                cursor.execute(
                    "INSERT INTO milestones (ticket_id, event_type, user_id, user_role, created_at) VALUES (?, ?, ?, ?, ?)",
                    (ticket.id, milestone.event_type.name, milestone.user.id if milestone.user else None,
                     self._role(milestone.user), milestone.created_at.isoformat())
                )
                milestone.id = cursor.lastrowid
        for message in ticket.messages:
            if message.id is None:
                cursor.execute(
                    "INSERT INTO messages (ticket_id, content, sender_id, sender_role, read, created_at) VALUES (?, ?, ?, ?, ?, ?)",
                    (ticket.id, message.content, message.sender.id if message.sender else None,
                     self._role(message.sender), int(message.read), message.created_at.isoformat())
                )
                message.id = cursor.lastrowid
            else:                                       # los mensajes existentes solo cambian su estado "leido"
                cursor.execute("UPDATE messages SET read = ? WHERE id = ?", (int(message.read), message.id))

    # ---------- leer ----------

    SELECT = """SELECT id, title, description, status, created_at, closed_at, category,
                priority, customer_id, agent_id, product_id FROM tickets"""

    def _to_ticket(self, row):
        (id, title, description, status, created_at, closed_at, category,
         priority, customer_id, agent_id, product_id) = row
        ticket = Ticket(id, title, description, TicketStatus[status], self._date(created_at))
        ticket.closed_at = self._date(closed_at)
        ticket.category = TicketCategory[category] if category else None
        ticket.priority = TicketPriority[priority] if priority else None
        ticket.customer = self._user("customer", customer_id)
        ticket.agent = self._user("agent", agent_id)
        if self.product_repo is not None and product_id is not None:
            ticket.product = self.product_repo.get_by_id(product_id)

        cursor = self.conn.cursor()
        cursor.execute(
            "SELECT id, event_type, user_id, user_role, created_at FROM milestones WHERE ticket_id = ? ORDER BY id",
            (id,)
        )
        for m_id, event_type, user_id, user_role, m_created in cursor.fetchall():
            ticket.milestones.append(
                Milestone(m_id, EventType[event_type], self._user(user_role, user_id), self._date(m_created))
            )
        cursor.execute(
            "SELECT id, content, sender_id, sender_role, read, created_at FROM messages WHERE ticket_id = ? ORDER BY id",
            (id,)
        )
        for msg_id, content, sender_id, sender_role, read, msg_created in cursor.fetchall():
            ticket.messages.append(
                Message(msg_id, content, self._user(sender_role, sender_id), bool(read), self._date(msg_created))
            )
        return ticket

    def list(self):                               
        cursor = self.conn.cursor()
        cursor.execute(self.SELECT + " ORDER BY id")
        rows = cursor.fetchall()
        return [self._to_ticket(row) for row in rows] # Se convierten las filas en objetos Tickets
    
    def get_by_id(self, id,):              
        cursor = self.conn.cursor()
        cursor.execute(self.SELECT + " WHERE id = ?", (id,))
        row = cursor.fetchone()

        if row:                            
            return self._to_ticket(row)
        return None
