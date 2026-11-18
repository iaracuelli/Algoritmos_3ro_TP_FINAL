# gui/agent_window.py
# Ventana principal del agente: tickets asignados y tickets sin asignar para tomar.

import tkinter as tk
from tkinter import ttk, messagebox
from gui.ticket_table import TicketTable
from gui.ticket_detail_window import TicketDetailWindow
from gui.helpers import REFRESH_MS
from gui.theme import make_header, center, SYSTEM_NAME

BASE_TITLE = "Soporte Técnico - Agente"


class AgentWindow(tk.Toplevel):
    def __init__(self, parent, controller, user, on_logout):
        super().__init__(parent)
        self.controller = controller
        self.user = user
        self.on_logout = on_logout

        self.title(BASE_TITLE)
        center(self, 1180, 720)
        self.minsize(950, 520)
        self.protocol("WM_DELETE_WINDOW", self.logout)

        make_header(self, SYSTEM_NAME, f"Agente  ·  {user.name}",
                    [("Cerrar sesión", self.logout), ("Actualizar", self.refresh)])

        main = ttk.Frame(self, padding=(28, 16))
        main.pack(fill="both", expand=True)

        notebook = ttk.Notebook(main)
        notebook.pack(fill="both", expand=True)

        # pestaña 1: tickets asignados
        mine = ttk.Frame(notebook, padding=(0, 16))
        notebook.add(mine, text="Mis tickets")
        self.table_mine = TicketTable(mine, user, on_open=lambda: self.open_detail(self.table_mine))
        self.table_mine.pack(fill="both", expand=True)
        ttk.Button(mine, text="Ver detalle", command=lambda: self.open_detail(self.table_mine),
                   style="Accent.TButton").pack(anchor="w", pady=(14, 0))

        # pestaña 2: tickets sin asignar
        free = ttk.Frame(notebook, padding=(0, 16))
        notebook.add(free, text="Sin asignar")
        self.table_free = TicketTable(free, user, on_open=lambda: self.open_detail(self.table_free))
        self.table_free.pack(fill="both", expand=True)
        buttons = ttk.Frame(free)
        buttons.pack(fill="x", pady=(14, 0))
        ttk.Button(buttons, text="Tomar ticket", command=self.take_ticket, style="Accent.TButton").pack(side="left")
        ttk.Button(buttons, text="Ver detalle", command=lambda: self.open_detail(self.table_free)).pack(side="left", padx=8)

        self._job = None
        self._auto_refresh()

    def _auto_refresh(self):
        # se actualiza sola cada unos segundos para ver los mensajes y tickets nuevos
        self.refresh()
        self._job = self.after(REFRESH_MS, self._auto_refresh)

    def refresh(self):
        tickets = self.controller.tickets_of(self.user)
        self.table_mine.load(tickets)
        self.table_free.load(self.controller.unassigned_tickets())
        unread = sum(t.unread_count(self.user) for t in tickets)
        self.title(BASE_TITLE + (f"  ({unread} mensaje{'s' if unread != 1 else ''} sin leer)" if unread else ""))

    def open_detail(self, table):
        ticket = table.selected()
        if ticket is None:
            messagebox.showinfo("Ticket", "Elegí un ticket de la lista", parent=self)
            return
        TicketDetailWindow(self, self.controller, self.user, ticket, on_change=self.refresh)

    def take_ticket(self):
        ticket = self.table_free.selected()
        if ticket is None:
            messagebox.showinfo("Ticket", "Elegí un ticket de la lista", parent=self)
            return
        try:
            self.controller.take_ticket(self.user, ticket)
        except Exception as e:
            messagebox.showerror("Error", str(e), parent=self)
            return
        self.refresh()

    def logout(self):
        if self._job:
            self.after_cancel(self._job)
        self.destroy()
        self.on_logout()
