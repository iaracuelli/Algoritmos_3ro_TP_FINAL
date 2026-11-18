# gui/login_window.py
# Ventana de login. Según el rol del usuario abre la ventana de cliente, agente o administrador.

import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from models.customer import Customer
from models.agent import Agent
from models.admin import Admin
from gui.customer_window import CustomerWindow
from gui.agent_window import AgentWindow
from gui.admin_window import AdminWindow
from gui.dialogs import ask_form
from gui.theme import apply_theme, center, SYSTEM_NAME, SYSTEM_SUBTITLE


class LoginWindow(tk.Tk):
    def __init__(self, controller):
        super().__init__()

        self.controller = controller

        apply_theme(self)                               # colores y estilos de todo el sistema
        self.title("Soporte Técnico - Ingreso")
        center(self, 520, 710)
        self.resizable(False, False)

        # franja naranja con el nombre del sistema
        banner = ttk.Frame(self, style="Header.TFrame", padding=(30, 34))
        banner.pack(fill="x")
        ttk.Label(banner, text=SYSTEM_NAME, style="Header.TLabel",
                  font=("Segoe UI", 26, "bold")).pack()
        ttk.Label(banner, text=SYSTEM_SUBTITLE, style="HeaderSub.TLabel").pack(pady=(4, 0))

        # tarjeta del formulario
        body = ttk.Frame(self, padding=(40, 30))
        body.pack(fill="both", expand=True)
        card = ttk.Frame(body, style="Card.TFrame", padding=(30, 26))
        card.pack(fill="x")

        ttk.Label(card, text="Iniciá sesión", style="CardH2.TLabel").pack(anchor="w", pady=(0, 16))

        ttk.Label(card, text="Email", style="CardBold.TLabel").pack(anchor="w", pady=(0, 4))
        self.entry_email = ttk.Entry(card, font=("Segoe UI", 11))
        self.entry_email.pack(fill="x", pady=(0, 14))

        ttk.Label(card, text="Contraseña", style="CardBold.TLabel").pack(anchor="w", pady=(0, 4))
        self.entry_password = ttk.Entry(card, show="*", font=("Segoe UI", 11))
        self.entry_password.pack(fill="x", pady=(0, 20))
        self.entry_password.bind("<Return>", lambda event: self.login())
        self.entry_email.bind("<Return>", lambda event: self.entry_password.focus_set())

        ttk.Button(card, text="Ingresar", command=self.login, style="Accent.TButton").pack(fill="x", ipady=3)

        ttk.Separator(card).pack(fill="x", pady=22)
        ttk.Label(card, text="¿Todavía no tenés cuenta?", style="CardMuted.TLabel").pack()
        ttk.Button(card, text="Crear cuenta de cliente", command=self.register).pack(fill="x", pady=(8, 0))

        ttk.Label(self, text="Trabajo final · Algoritmos y Estructuras de Datos III",
                  style="Muted.TLabel").pack(side="bottom", pady=(0, 14))

        self.entry_email.focus_set()

    
    def login(self):
        try:
            user = self.controller.login(
                self.entry_email.get().strip(),
                self.entry_password.get()
            )
        except Exception as e:
            messagebox.showerror("Error", str(e))
            return

        self.entry_password.delete(0, "end")
        self.withdraw()                                 # se oculta el login mientras dura la sesion

        if isinstance(user, Customer):
            CustomerWindow(self, self.controller, user, self.show_again)
        elif isinstance(user, Agent):
            AgentWindow(self, self.controller, user, self.show_again)
        elif isinstance(user, Admin):
            AdminWindow(self, self.controller, user, self.show_again)

    def show_again(self):
        self.deiconify()
        self.entry_password.focus_set()

    def register(self):
        def create(values):
            self.controller.create_customer(values["name"], values["email"], values["password"])
            messagebox.showinfo("Cuenta creada", "Ya podés ingresar con tu email y contraseña")
            self.entry_email.delete(0, "end")
            self.entry_email.insert(0, values["email"])

        ask_form(self, "Crear cuenta de cliente", [
            ("Nombre", "name", "entry"),
            ("Email", "email", "entry"),
            ("Contraseña", "password", "password"),
        ], create, "Crear cuenta")
