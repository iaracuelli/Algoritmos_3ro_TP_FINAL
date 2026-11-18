# gui/ticket_table.py
# Tabla de tickets que usan las ventanas de cliente, agente y administrador.
# Incluye una barra de filtros (búsqueda de texto, estado, prioridad y producto).

from tkinter import ttk
from models.admin import Admin
from models.ticket_status import TicketStatus
from models.ticket_priority import TicketPriority
from gui.helpers import make_tree

COLUMNS = [
    ("id", "ID", 50),
    ("title", "Título", 260),
    ("customer", "Cliente", 140),
    ("product", "Producto", 140),
    ("priority", "Prioridad", 95),
    ("status", "Estado", 110),
    ("agent", "Agente", 140),
    ("unread", "Sin leer", 80),
]

ALL = "Todos"


class TicketTable(ttk.Frame):
    def __init__(self, parent, user, on_open=None):
        super().__init__(parent)
        self.user = user
        self.all_tickets = []           # todos los tickets recibidos
        self.tickets = {}               # los que se están mostrando (id -> ticket)

        self._build_filters()
        frame, self.tree = make_tree(self, COLUMNS)
        frame.pack(fill="both", expand=True)
        if on_open:
            self.tree.bind("<Double-1>", lambda event: on_open())

    def _build_filters(self):
        bar = ttk.Frame(self)
        bar.pack(fill="x", pady=(0, 10))

        self.lbl_count = ttk.Label(bar, style="Muted.TLabel")
        self.lbl_count.pack(side="right")               # se empaqueta primero para que siempre tenga lugar

        ttk.Label(bar, text="Buscar:").pack(side="left")
        self.entry_search = ttk.Entry(bar, width=15)
        self.entry_search.pack(side="left", padx=(6, 12))
        self.entry_search.bind("<KeyRelease>", lambda event: self.apply_filters())

        self.combo_status = self._combo(bar, "Estado:", [s.value for s in TicketStatus], 10)
        self.combo_priority = self._combo(bar, "Prioridad:", [p.value for p in TicketPriority], 8)
        self.combo_product = self._combo(bar, "Producto:", [], 13)

        ttk.Button(bar, text="Limpiar", command=self.clear_filters).pack(side="left")

    def _combo(self, bar, label, values, width):
        ttk.Label(bar, text=label).pack(side="left")
        combo = ttk.Combobox(bar, state="readonly", width=width, values=[ALL] + values)
        combo.set(ALL)
        combo.pack(side="left", padx=(6, 12))
        combo.bind("<<ComboboxSelected>>", lambda event: self.apply_filters())
        return combo

    # datos 

    def load(self, tickets):
        self.all_tickets = list(tickets)
        # el filtro de producto se arma con los productos que aparecen en los tickets
        products = sorted({t.product.name for t in self.all_tickets if t.product})
        self.combo_product.config(values=[ALL] + products)
        if self.combo_product.get() not in [ALL] + products:
            self.combo_product.set(ALL)
        self.apply_filters()

    def clear_filters(self):
        self.entry_search.delete(0, "end")
        for combo in (self.combo_status, self.combo_priority, self.combo_product):
            combo.set(ALL)
        self.apply_filters()

    def _matches(self, t):
        text = self.entry_search.get().strip().lower()
        if text:
            haystack = " ".join([
                str(t.id), t.title,
                t.customer.name if t.customer else "",
                t.agent.name if t.agent else "",
                t.product.name if t.product else "",
            ]).lower()
            if text not in haystack:
                return False
        if self.combo_status.get() != ALL and t.status.value != self.combo_status.get():
            return False
        if self.combo_priority.get() != ALL and (not t.priority or t.priority.value != self.combo_priority.get()):
            return False
        if self.combo_product.get() != ALL and (not t.product or t.product.name != self.combo_product.get()):
            return False
        return True

    def apply_filters(self):
        shown = [t for t in self.all_tickets if self._matches(t)]
        self.lbl_count.config(text=f"Mostrando {len(shown)} de {len(self.all_tickets)}")
        self._show(shown)

    def _show(self, tickets):
        previous = self.tree.selection()                # para no perder la selección al refrescar
        self.tree.delete(*self.tree.get_children())
        self.tickets = {}
        for i, t in enumerate(tickets):
            unread = "-" if isinstance(self.user, Admin) else t.unread_count(self.user)
            self.tickets[str(t.id)] = t
            tags = ["odd"] if i % 2 else []
            if unread != "-" and unread > 0:
                tags.append("unread")                   # los tickets con mensajes sin leer se ven en negrita
            self.tree.insert("", "end", iid=str(t.id), tags=tags, values=(
                t.id,
                t.title,
                t.customer.name if t.customer else "-",
                t.product.name if t.product else "-",
                t.priority.value if t.priority else "-",
                t.status.value,
                t.agent.name if t.agent else "Sin asignar",
                unread,
            ))
        if previous and previous[0] in self.tickets:
            self.tree.selection_set(previous[0])

    def selected(self):
        selection = self.tree.selection()
        return self.tickets.get(selection[0]) if selection else None
