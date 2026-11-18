# gui/admin_window.py
# Ventana principal del administrador: tickets (asignar/reasignar), clientes, agentes y productos.

import tkinter as tk
from tkinter import ttk, messagebox
from gui.ticket_table import TicketTable
from gui.ticket_detail_window import TicketDetailWindow
from gui.dialogs import ask_form
from gui.helpers import make_tree, stripe, REFRESH_MS
from gui.theme import make_header, center, SYSTEM_NAME


class AdminWindow(tk.Toplevel):
    def __init__(self, parent, controller, user, on_logout):
        super().__init__(parent)
        self.controller = controller
        self.user = user
        self.on_logout = on_logout

        self.title("Soporte Técnico - Administrador")
        center(self, 1180, 720)
        self.minsize(950, 520)
        self.protocol("WM_DELETE_WINDOW", self.logout)

        make_header(self, SYSTEM_NAME, f"Administrador  ·  {user.name}",
                    [("Cerrar sesión", self.logout), ("Actualizar", self.refresh)])

        main = ttk.Frame(self, padding=(28, 16))
        main.pack(fill="both", expand=True)

        notebook = ttk.Notebook(main)
        notebook.pack(fill="both", expand=True)

        self._build_tickets_tab(notebook)
        self.tree_customers = self._build_people_tab(notebook, "Clientes", None)
        self.tree_agents = self._build_people_tab(notebook, "Agentes", self.new_agent)
        self._build_products_tab(notebook)

        self._job = None
        self._auto_refresh()

    def _auto_refresh(self):
        # se actualiza sola cada unos segundos
        self.refresh()
        self._job = self.after(REFRESH_MS, self._auto_refresh)

    # pestañas

    def _build_tickets_tab(self, notebook):
        tab = ttk.Frame(notebook, padding=(0, 16))
        notebook.add(tab, text="Tickets")
        self.table = TicketTable(tab, self.user, on_open=self.open_detail)
        self.table.pack(fill="both", expand=True)
        buttons = ttk.Frame(tab)
        buttons.pack(fill="x", pady=(14, 0))
        ttk.Button(buttons, text="Asignar / Reasignar agente", command=self.assign, style="Accent.TButton").pack(side="left")
        ttk.Button(buttons, text="Ver detalle", command=self.open_detail).pack(side="left", padx=8)

    def _build_people_tab(self, notebook, title, on_new):
        tab = ttk.Frame(notebook, padding=(0, 16))
        notebook.add(tab, text=title)
        frame, tree = make_tree(tab, [("id", "ID", 60), ("name", "Nombre", 260),
                                      ("email", "Email", 340), ("active", "Estado", 120)])
        frame.pack(fill="both", expand=True)
        buttons = ttk.Frame(tab)
        buttons.pack(fill="x", pady=(14, 0))
        if on_new:
            ttk.Button(buttons, text="+  Nuevo agente", command=on_new, style="Accent.TButton").pack(side="left", padx=(0, 8))
        ttk.Button(buttons, text="Activar", command=lambda: self.set_active(tree, True)).pack(side="left")
        ttk.Button(buttons, text="Desactivar", command=lambda: self.set_active(tree, False)).pack(side="left", padx=8)
        tree.people = {}                                # id -> usuario
        return tree

    def _build_products_tab(self, notebook):
        tab = ttk.Frame(notebook, padding=(0, 16))
        notebook.add(tab, text="Productos")
        frame, self.tree_products = make_tree(tab, [("id", "ID", 60), ("name", "Producto", 320), ("category", "Rubro", 260)])
        frame.pack(fill="both", expand=True)
        ttk.Button(tab, text="+  Nuevo producto", command=self.new_product, style="Accent.TButton").pack(anchor="w", pady=(14, 0))

    # datos 

    def refresh(self):
        self.table.load(self.controller.tickets_of(self.user))
        self._load_people(self.tree_customers, self.controller.list_customers())
        self._load_people(self.tree_agents, self.controller.list_agents())
        self.tree_products.delete(*self.tree_products.get_children())
        for p in self.controller.list_products():
            self.tree_products.insert("", "end", values=(p.id, p.name, p.category.name if p.category else "-"))
        stripe(self.tree_products)

    def _load_people(self, tree, people):
        previous = tree.selection()                     # para no perder la selección al refrescar
        tree.delete(*tree.get_children())
        tree.people = {}
        for p in people:
            tree.people[str(p.id)] = p
            tree.insert("", "end", iid=str(p.id), values=(p.id, p.name, p.email, "Activo" if p.active else "Inactivo"))
        stripe(tree)
        if previous and previous[0] in tree.people:
            tree.selection_set(previous[0])

    # acciones 

    def open_detail(self):
        ticket = self.table.selected()
        if ticket is None:
            messagebox.showinfo("Ticket", "Elegí un ticket de la lista", parent=self)
            return
        TicketDetailWindow(self, self.controller, self.user, ticket, on_change=self.refresh)

    def assign(self):
        ticket = self.table.selected()
        if ticket is None:
            messagebox.showinfo("Ticket", "Elegí un ticket de la lista", parent=self)
            return
        agents = {f"{a.name} ({a.email})": a for a in self.controller.list_agents() if a.active}
        if not agents:
            messagebox.showinfo("Agentes", "No hay agentes activos", parent=self)
            return

        def do_assign(values):
            agent = agents[values["agent"]]
            if ticket.agent is None:
                self.controller.assign_ticket(self.user, agent, ticket)
            else:
                self.controller.reassign_ticket(self.user, ticket.agent, agent, ticket)
            self.refresh()

        current = ticket.agent.name if ticket.agent else "sin asignar"
        ask_form(self, f"Ticket #{ticket.id} (actual: {current})", [
            ("Agente", "agent", "combo", list(agents)),
        ], do_assign, "Asignar")

    def set_active(self, tree, active):
        selection = tree.selection()
        if not selection:
            messagebox.showinfo("Usuario", "Elegí un usuario de la lista", parent=self)
            return
        self.controller.set_active(self.user, tree.people[selection[0]], active)
        self.refresh()

    def new_agent(self):
        def create(values):
            self.controller.create_agent(values["name"], values["email"], values["password"])
            self.refresh()

        ask_form(self, "Nuevo agente", [
            ("Nombre", "name", "entry"),
            ("Email", "email", "entry"),
            ("Contraseña", "password", "password"),
        ], create, "Crear agente")

    def new_product(self):
        categories = [c.name for c in self.controller.list_categories()]

        def create(values):
            self.controller.create_product(values["name"], values["category"])
            self.refresh()

        ask_form(self, "Nuevo producto", [
            ("Producto", "name", "entry"),
            ("Rubro (elegí uno o escribí uno nuevo)", "category", "combo_free", categories),
        ], create, "Crear producto")

    def logout(self):
        if self._job:
            self.after_cancel(self._job)
        self.destroy()
        self.on_logout()
