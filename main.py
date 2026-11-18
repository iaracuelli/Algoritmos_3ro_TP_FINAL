import os
from models.admin import Admin
from managers.agent_manager import AgentManager
from managers.customer_manager import CustomerManager
from managers.ticket_manager import TicketManager
from managers.product_manager import ProductManager
from controllers.ticket_controller import TicketController
from persistence.customerRepositoryDB import CustomerRepositoryDB
from persistence.agentRepositoryDB import AgentRepositoryDB
from persistence.ticketRepositoryDB import TicketRepositoryDB
from persistence.adminRepositoryDB import AdminRepositoryDB
from persistence.productRepositoryDB import ProductRepositoryDB
from gui.login_window import LoginWindow

# Una sola base de datos SQLite, junto a main.py
DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "ticketing.db")

# Rubros y productos iniciales (el admin puede agregar más desde su ventana)
INITIAL_PRODUCTS = {
    "Cocina": ["Heladera", "Cocina", "Horno eléctrico", "Microondas"],
    "Lavado": ["Lavarropas", "Secarropas"],
    "Climatización": ["Aire acondicionado", "Calefactor"],
}

def main():
    # creo los repositorios
    repo_admin = AdminRepositoryDB(DB_PATH)
    repo_customers = CustomerRepositoryDB(DB_PATH)
    repo_agents = AgentRepositoryDB(DB_PATH)
    repo_products = ProductRepositoryDB(DB_PATH)
    repo_tickets = TicketRepositoryDB(DB_PATH, repo_customers, repo_agents, repo_admin, repo_products)
    
    # creo los managers
    customer_manager = CustomerManager(repo_customers)
    agent_manager = AgentManager(repo_agents)
    ticket_manager = TicketManager(repo_tickets)
    product_manager = ProductManager(repo_products)


    # crear admin por defecto si no existe ninguno
    if not repo_admin.list():
        repo_admin.save(Admin(None, "Admin", "admin@sistema.com", "admin123"))

    # cargar rubros y productos iniciales si no hay ninguno
    if not product_manager.list_products():
        for category_name, product_names in INITIAL_PRODUCTS.items():
            category = product_manager.create_category(category_name)
            for product_name in product_names:
                product_manager.create_product(product_name, category)

    # creo el controlador inyectando los managers
    controller = TicketController(
        ticket_manager,
        customer_manager,
        agent_manager,
        product_manager,
        repo_admin
    )

    print("Sistema iniciado")


    app = LoginWindow(controller)
    app.mainloop()


if __name__ == "__main__":
    main()
