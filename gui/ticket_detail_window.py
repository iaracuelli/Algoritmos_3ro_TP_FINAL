# gui/ticket_detail_window.py
# Detalle de un ticket: datos, mensajes, historial (hitos) y acciones según el rol.

import tkinter as tk
from tkinter import ttk, messagebox
from models.customer import Customer
from models.agent import Agent
from models.admin import Admin
from models.ticket_status import TicketStatus
from models.ticket_category import TicketCategory
from models.ticket_priority import TicketPriority
from gui.helpers import role_name, fmt_date, REFRESH_MS
from gui.theme import make_header, center, style_text, PRIMARY_DEEP, FONT_BOLD


class TicketDetailWindow(tk.Toplevel):
    def __init__(self, parent, controller, user, ticket, on_change=None):
        super().__init__(parent)
        self.controller = controller
        self.user = user
        self.on_change = on_change
        # al abrir el ticket se marcan como leidos los mensajes de la otra parte
        self.ticket = controller.view_ticket(user, ticket)

        self.title(f"Ticket #{ticket.id}")
        center(self, 920, 900)
        self.minsize(780, 700)
        self._shown = None              # (estado, prioridad, categoría) que muestran los combos
        self._last_sig = None           # para saber si el ticket cambio desde la última vez
        self._job = None
        self._build()
        self.refresh()
        if self.on_change:
            self.on_change()
        self.bind("<Destroy>", self._on_destroy)
        self._job = self.after(REFRESH_MS, self._auto_refresh)

    def _on_destroy(self, event):
        if event.widget is self and self._job:
            self.after_cancel(self._job)
            self._job = None

    def _signature(self):
        t = self.ticket
        return (t.status, t.priority, t.category, t.agent.id if t.agent else None,
                len(t.messages), len(t.milestones))

    def _auto_refresh(self):
        # vuelve a leer el ticket de la base: si la otra parte escribio o cambio algo, se actualiza sola
        fresh = self.controller.get_ticket_by_id(self.ticket.id)
        if fresh is not None:
            if fresh.unread_count(self.user) > 0:
                fresh = self.controller.view_ticket(self.user, fresh)   # la ventana esta abierta: se leen
            self.ticket = fresh
            if self._signature() != self._last_sig:
                self.refresh()
                if self.on_change:
                    self.on_change()
        self._job = self.after(REFRESH_MS, self._auto_refresh)

    # armado 

    def _build(self):
        _, self.hdr_title, self.hdr_subtitle = make_header(self, f"Ticket #{self.ticket.id}", self.ticket.title)

        main = ttk.Frame(self, padding=(28, 18))
        main.pack(fill="both", expand=True)

        # tarjeta con los datos del ticket
        card = ttk.Frame(main, style="Card.TFrame", padding=(20, 14))
        card.pack(fill="x")
        self.info = {}
        fields = [("Estado", "status"), ("Prioridad", "priority"), ("Cliente", "customer"),
                  ("Agente", "agent"), ("Producto", "product"), ("Categoría", "category"),
                  ("Creado", "created"), ("Cerrado", "closed")]
        for i, (label, key) in enumerate(fields):
            row, col = divmod(i, 2)
            ttk.Label(card, text=label, style="CardMuted.TLabel").grid(
                row=row * 2, column=col, sticky="w", padx=(0, 40), pady=(6, 0))
            self.info[key] = ttk.Label(card, style="CardBold.TLabel")
            self.info[key].grid(row=row * 2 + 1, column=col, sticky="w", padx=(0, 40))
        ttk.Label(card, text="Descripción", style="CardMuted.TLabel").grid(
            row=8, column=0, columnspan=2, sticky="w", pady=(10, 0))
        self.lbl_description = ttk.Label(card, style="Card.TLabel", wraplength=800, justify="left")
        self.lbl_description.grid(row=9, column=0, columnspan=2, sticky="w")

        notebook = ttk.Notebook(main)
        notebook.pack(fill="both", expand=True, pady=(14, 0))
        self.txt_messages = self._text_tab(notebook, "Mensajes")
        self.txt_history = self._text_tab(notebook, "Historial")

        # cambiar prioridad y categoria (agente y administrador)
        if isinstance(self.user, (Agent, Admin)):
            edit = ttk.Frame(main)
            edit.pack(fill="x", pady=(12, 0))
            ttk.Label(edit, text="Prioridad").pack(side="left")
            self.combo_priority = ttk.Combobox(edit, state="readonly", width=11,
                                               values=[p.value for p in TicketPriority])
            self.combo_priority.pack(side="left", padx=(8, 18))
            ttk.Label(edit, text="Categoría").pack(side="left")
            self.combo_category = ttk.Combobox(edit, state="readonly", width=17,
                                               values=[c.value for c in TicketCategory])
            self.combo_category.pack(side="left", padx=(8, 18))
            ttk.Button(edit, text="Guardar cambios", command=self._save_info).pack(side="left")

        # enviar mensaje (cliente y agente)
        if isinstance(self.user, (Customer, Agent)):
            send = ttk.Frame(main)
            send.pack(fill="x", pady=(12, 0))
            self.entry_message = ttk.Entry(send, font=("Segoe UI", 11))
            self.entry_message.pack(side="left", fill="x", expand=True)
            self.entry_message.bind("<Return>", lambda event: self._send())
            self.btn_send = ttk.Button(send, text="Enviar", command=self._send, style="Accent.TButton")
            self.btn_send.pack(side="left", padx=(8, 0))

        # acciones
        actions = ttk.Frame(main)
        actions.pack(fill="x", pady=(14, 0))
        if isinstance(self.user, Agent):
            ttk.Label(actions, text="Estado").pack(side="left")
            self.combo_status = ttk.Combobox(actions, state="readonly", width=14,
                                             values=[s.value for s in TicketStatus])
            self.combo_status.pack(side="left", padx=8)
            ttk.Button(actions, text="Cambiar estado", command=self._change_status).pack(side="left")
        if isinstance(self.user, (Customer, Agent)):
            self.btn_close = ttk.Button(actions, text="Cerrar ticket", command=self._close)
            self.btn_close.pack(side="left", padx=(18, 8))
            self.btn_reopen = ttk.Button(actions, text="Reabrir ticket", command=self._reopen)
            self.btn_reopen.pack(side="left")
        ttk.Button(actions, text="Cerrar ventana", command=self.destroy).pack(side="right")

    def _text_tab(self, notebook, title):
        frame = ttk.Frame(notebook, padding=(0, 12, 0, 0))
        notebook.add(frame, text=title)
        text = tk.Text(frame, wrap="word", state="disabled", height=12)
        style_text(text)
        scroll = ttk.Scrollbar(frame, orient="vertical", command=text.yview)
        text.configure(yscrollcommand=scroll.set)
        text.tag_configure("header", font=FONT_BOLD, foreground=PRIMARY_DEEP)
        text.pack(side="left", fill="both", expand=True)
        scroll.pack(side="right", fill="y")
        return text

    # mostrar datos 

    def refresh(self):
        t = self.ticket
        self.hdr_subtitle.config(text=t.title)
        self.info["status"].config(text=t.status.value)
        self.info["priority"].config(text=t.priority.value if t.priority else "-")
        self.info["customer"].config(text=t.customer.name if t.customer else "-")
        self.info["agent"].config(text=t.agent.name if t.agent else "Sin asignar")
        self.info["product"].config(text=t.product.name if t.product else "-")
        self.info["category"].config(text=t.category.value if t.category else "-")
        self.info["created"].config(text=fmt_date(t.created_at))
        self.info["closed"].config(text=fmt_date(t.closed_at))
        self.lbl_description.config(text=t.description)

        self._fill(self.txt_messages, [
            (f"{self._user_name(m.sender)} ({role_name(m.sender)}) - {fmt_date(m.created_at)}", m.content)
            for m in t.getMessages()
        ], "Todavía no hay mensajes.")
        self._fill(self.txt_history, [
            (f"{fmt_date(m.created_at)} - {m.event_type.value}", f"por {self._user_name(m.user)} ({role_name(m.user)})")
            for m in t.getMilestones()
        ], "Sin hitos registrados.")

        closed = t.status == TicketStatus.Closed
        if isinstance(self.user, (Customer, Agent)):
            self.btn_send.config(state="disabled" if closed else "normal")
            self.btn_close.config(state="disabled" if closed else "normal")
            self.btn_reopen.config(state="normal" if closed else "disabled")

        # los combos se reinician solo si el ticket cambio (asi no se pisa lo que se esta eligiendo)
        current = (t.status, t.priority, t.category)
        if current != self._shown:
            self._shown = current
            if isinstance(self.user, Agent):
                self.combo_status.set(t.status.value)
            if isinstance(self.user, (Agent, Admin)):
                self.combo_priority.set(t.priority.value if t.priority else "")
                self.combo_category.set(t.category.value if t.category else "")
        self._last_sig = self._signature()

    def _user_name(self, user):
        return user.name if user else "?"

    def _fill(self, widget, entries, empty_text):
        widget.config(state="normal")
        widget.delete("1.0", "end")
        if not entries:
            widget.insert("end", empty_text)
        for header, body in entries:
            widget.insert("end", header + "\n", "header")
            widget.insert("end", body + "\n\n")
        widget.config(state="disabled")
        widget.see("end")

    # acciones 

    def _run(self, action):
        try:
            action()
        except Exception as e:
            messagebox.showerror("Error", str(e), parent=self)
            return
        self.refresh()
        if self.on_change:
            self.on_change()

    def _send(self):
        def action():
            self.controller.send_message(self.user, self.ticket, self.entry_message.get())
            self.entry_message.delete(0, "end")
        self._run(action)

    def _close(self):
        self._run(lambda: self.controller.close_ticket(self.user, self.ticket))

    def _reopen(self):
        self._run(lambda: self.controller.reopen_ticket(self.user, self.ticket))

    def _save_info(self):
        priority = next((p for p in TicketPriority if p.value == self.combo_priority.get()), None)
        category = next((c for c in TicketCategory if c.value == self.combo_category.get()), None)
        self._run(lambda: self.controller.update_ticket_info(self.user, self.ticket, category, priority))

    def _change_status(self):
        status = next(s for s in TicketStatus if s.value == self.combo_status.get())
        self._run(lambda: self.controller.update_status(self.user, self.ticket, status))
