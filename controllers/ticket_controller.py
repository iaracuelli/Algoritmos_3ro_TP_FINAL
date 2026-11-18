# controllers/ticket_controller.py
# Se encarga de coordinar la interacción entre el usuario
# y los gestores del dominio (clientes, agente y admin).

from models.customer import Customer
from models.agent import Agent
from models.admin import Admin
from models.ticket_status import TicketStatus


class TicketController:
    def __init__(self, ticket_manager, customer_manager, agent_manager, product_manager, admin_repository):
        self.ticket_manager = ticket_manager
        self.customer_manager = customer_manager
        self.agent_manager = agent_manager
        self.product_manager = product_manager
        self.admin_repository = admin_repository

        
    def login(self, email, password):
        user = self._find_user(email, password)
        if not getattr(user, "active", True):
            raise Exception("Usuario inactivo")
        self._load_tickets(user)
        return user

    def _find_user(self, email, password):
        #busca admin
        for admin in self.admin_repository.list():
            if admin.email == email and admin.login(password):
                return admin
            
        # buscar en customers
        for customer in self.customer_manager.list_customers():
            if customer.email == email and customer.login(password):
                return customer  
        
        # buscar en agents
        for agent in self.agent_manager.list_agents():
            if agent.email == email and agent.login(password):
                return agent
        
        # si no encontró nadie
        raise Exception("Usuario no encontrado")

    def _load_tickets(self, user):
        # carga en el usuario sus tickets desde la base (Customer y Agent tienen la lista tickets)
        tickets = self.ticket_manager.list_tickets()
        if isinstance(user, Customer):
            user.tickets = [t for t in tickets if t.customer is not None and t.customer.id == user.id]
        elif isinstance(user, Agent):
            user.tickets = [t for t in tickets if t.agent is not None and t.agent.id == user.id]

    # ---------- altas ----------

    def create_customer(self, name, email, password):
        self._check_required(name, email, password)
        return self.customer_manager.create_customer(name, email, password)

    def create_agent(self, name, email, password):
        self._check_required(name, email, password)
        return self.agent_manager.create_agent(name, email, password)

    def _check_required(self, name, email, password):
        if not name.strip() or not email.strip() or not password.strip():
            raise Exception("Completá nombre, email y contraseña")

    def create_ticket(self, customer, title, description, product, category, priority):
        if not title.strip() or not description.strip():
            raise Exception("Completá el título y la descripción")
        if product is None or category is None or priority is None:
            raise Exception("Elegí producto, categoría y prioridad")
        ticket = self.ticket_manager.create_ticket(
            title.strip(), description.strip(),
            customer=customer, product=product, category=category, priority=priority
        )
        customer.tickets.append(ticket)
        return ticket

    # ---------- consultas ----------

    def list_tickets(self):                  
        return self.ticket_manager.list_tickets()

    def get_ticket_by_id(self, id):
        return self.ticket_manager.get_ticket_by_id(id)

    def tickets_of(self, user):
        # tickets que ve cada rol: el cliente los suyos, el agente los asignados, el admin todos
        self._load_tickets(user)
        if isinstance(user, Admin):
            return self.ticket_manager.list_tickets()
        return user.tickets

    def unassigned_tickets(self):
        return [t for t in self.ticket_manager.list_tickets()
                if t.agent is None and t.status != TicketStatus.Closed]

    def list_customers(self):
        return self.customer_manager.list_customers()

    def list_agents(self):
        return self.agent_manager.list_agents()

    def list_products(self):
        return self.product_manager.list_products()

    def list_categories(self):
        return self.product_manager.list_categories()

    # ---------- trabajo sobre un ticket ----------

    def view_ticket(self, user, ticket):
        # al abrir el ticket se marcan como leídos los mensajes de la otra parte
        if isinstance(user, (Customer, Agent)):
            user.viewDetailTicket(ticket)
            self.ticket_manager.update_ticket(ticket)
        return ticket

    def send_message(self, user, ticket, content):
        if not content.strip():
            raise Exception("Escribí un mensaje")
        if isinstance(user, Customer):
            user.sendMessage(ticket, content.strip())
        elif isinstance(user, Agent):
            user.respondTicket(ticket, content.strip())
        else:
            raise Exception("El administrador no envía mensajes")
        self.ticket_manager.update_ticket(ticket)

    def close_ticket(self, user, ticket):
        user.closeTicket(ticket)
        self.ticket_manager.update_ticket(ticket)

    def reopen_ticket(self, user, ticket):
        if isinstance(user, Customer):
            user.reopenTicket(ticket)
        else:
            ticket.reopen(user)
        self.ticket_manager.update_ticket(ticket)

    def update_status(self, agent, ticket, status):
        agent.updateStatus(ticket, status)
        self.ticket_manager.update_ticket(ticket)

    def update_ticket_info(self, user, ticket, category, priority):
        # solo el agente o el administrador pueden cambiar la categoría y la prioridad
        if not isinstance(user, (Agent, Admin)):
            raise Exception("No tenés permiso para modificar el ticket")
        if ticket.updateInfo(category, priority, user):
            self.ticket_manager.update_ticket(ticket)

    def take_ticket(self, agent, ticket):
        if ticket.agent is not None:
            raise Exception("El ticket ya tiene un agente asignado")
        agent.take_ticket(ticket)
        self.ticket_manager.update_ticket(ticket)

    def assign_ticket(self, admin, agent, ticket):
        admin.assignTicket(agent, ticket)
        self.ticket_manager.update_ticket(ticket)

    def reassign_ticket(self, admin, agent1, agent2 ,ticket):
        admin.reassignTicket(agent1, agent2, ticket)
        self.ticket_manager.update_ticket(ticket)

    # ---------- administración ----------

    def set_active(self, admin, user, active):
        if isinstance(user, Customer):
            admin.activateCustomer(user) if active else admin.deactivateCustomer(user)
            self.customer_manager.update_customer(user)
        elif isinstance(user, Agent):
            admin.activateAgent(user) if active else admin.deactivateAgent(user)
            self.agent_manager.update_agent(user)

    def create_product(self, name, category_name):
        if not name.strip() or not category_name.strip():
            raise Exception("Completá el nombre del producto y el rubro")
        category = None
        for existing in self.product_manager.list_categories():
            if existing.name == category_name.strip():
                category = existing
        if category is None:                        # si el rubro no existe, se crea
            category = self.product_manager.create_category(category_name.strip())
        return self.product_manager.create_product(name.strip(), category)
