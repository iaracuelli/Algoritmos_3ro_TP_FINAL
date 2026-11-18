# gui/helpers.py
# Funciones chicas que usan varias ventanas.

import tkinter as tk
from tkinter import ttk
from models.customer import Customer
from models.agent import Agent
from models.admin import Admin
from gui.theme import STRIPE, PRIMARY_DEEP, FONT_BOLD

REFRESH_MS = 5000       # cada cuantos milisegundos se actualizan solas las ventanas


def role_name(user):
    if isinstance(user, Customer):
        return "Cliente"
    if isinstance(user, Agent):
        return "Agente"
    if isinstance(user, Admin):
        return "Administrador"
    return "-"


def fmt_date(date):
    return date.strftime("%d/%m/%Y %H:%M") if date else "-"


def make_tree(parent, columns, height=14):
    # columns: lista de (clave, titulo, ancho). Devuelve el Treeview ya armado con su scroll.
    frame = ttk.Frame(parent)
    tree = ttk.Treeview(frame, columns=[c[0] for c in columns], show="headings", height=height)
    for key, title, width in columns:
        tree.heading(key, text=title)
        tree.column(key, width=width, anchor="w")
    tree.tag_configure("odd", background=STRIPE)                       # filas alternadas
    tree.tag_configure("unread", foreground=PRIMARY_DEEP, font=FONT_BOLD)   # tickets con mensajes sin leer
    scroll = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=scroll.set)
    tree.pack(side="left", fill="both", expand=True)
    scroll.pack(side="right", fill="y")
    return frame, tree


def stripe(tree):
    for i, iid in enumerate(tree.get_children()):
        tree.item(iid, tags=("odd",) if i % 2 else ())
