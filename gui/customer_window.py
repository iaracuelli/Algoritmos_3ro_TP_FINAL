# gui/customer_window.py
# Ventana principal del cliente: sus tickets y la creación de nuevos.

import tkinter as tk
from tkinter import ttk, messagebox
from models.ticket_category import TicketCategory
from models.ticket_priority import TicketPriority
from gui.ticket_table import TicketTable
from gui.ticket_detail_window import TicketDetailWindow
from gui.dialogs import ask_form
from gui.helpers import REFRESH_MS
from gui.theme import make_header, center, SYSTEM_NAME

BASE_TITLE = "Soporte Técnico - Cliente"


class CustomerWindow(tk.Toplevel):
    def __init__(self, parent, controller, user, on_logout):
        super().__init__(parent)
        self.controller = controller
        self.user = user
        self.on_logout = on_logout

        self.title(BASE_TITLE)
        center(self, 1120, 680)
        self.minsize(900, 500)
        self.protocol("WM_DELETE_WINDOW", self.logout)

        make_header(self, SYSTEM_NAME, f"Cliente  ·  {user.name}",
                    [("Cerrar sesión", self.logout), ("Actualizar", self.refresh)])

        main = ttk.Frame(self, padding=(28, 20))
        main.pack(fill="both", expand=True)

        ttk.Label(main, text="Mis tickets", style="H2.TLabel").pack(anchor="w", pady=(0, 10))
        self.table = TicketTable(main, user, on_open=self.open_detail)
        self.table.pack(fill="both", expand=True)

        buttons = ttk.Frame(main)
        buttons.pack(fill="x", pady=(14, 0))
        ttk.Button(buttons, text="+  Nuevo ticket", command=self.new_ticket, style="Accent.TButton").pack(side="left")
        ttk.Button(buttons, text="Ver detalle", command=self.open_detail).pack(side="left", padx=8)

        self._job = None
        self._auto_refresh()

    def _auto_refresh(self):
        # se actualiza sola cada unos segundos para ver los mensajes nuevos
        self.refresh()
        self._job = self.after(REFRESH_MS, self._auto_refresh)

    def refresh(self):
        tickets = self.controller.tickets_of(self.user)
        self.table.load(tickets)
        unread = sum(t.unread_count(self.user) for t in tickets)
        self.title(BASE_TITLE + (f"  ({unread} mensaje{'s' if unread != 1 else ''} sin leer)" if unread else ""))

    def open_detail(self):
        ticket = self.table.selected()
        if ticket is None:
            messagebox.showinfo("Ticket", "Elegí un ticket de la lista", parent=self)
            return
        TicketDetailWindow(self, self.controller, self.user, ticket, on_change=self.refresh)

    def new_ticket(self):
        products = {p.name: p for p in self.controller.list_products()}
        categories = {c.value: c for c in TicketCategory}
        priorities = {p.value: p for p in TicketPriority}

        def create(values):
            self.controller.create_ticket(
                self.user, values["title"], values["description"],
                products.get(values["product"]),
                categories.get(values["category"]),
                priorities.get(values["priority"]),
            )
            self.refresh()

        ask_form(self, "Nuevo ticket", [
            ("Título", "title", "entry"),
            ("Descripción del problema", "description", "text"),
            ("Producto", "product", "combo", list(products)),
            ("Categoría", "category", "combo", list(categories)),
            ("Prioridad", "priority", "combo", list(priorities), TicketPriority.Medium.value),
        ], create, "Crear ticket")

    def logout(self):
        if self._job:
            self.after_cancel(self._job)
        self.destroy()
        self.on_logout()
