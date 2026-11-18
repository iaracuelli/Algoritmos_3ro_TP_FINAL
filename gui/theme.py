# gui/theme.py
# Colores, tipografía y estilos de todo el sistema (paleta naranja cálida).
# Se aplica una sola vez con apply_theme(); después las ventanas solo usan los estilos.

import tkinter as tk
from tkinter import ttk

#paleta 
PRIMARY = "#E8710A"          # naranja principal
PRIMARY_DARK = "#B85A00"
PRIMARY_DEEP = "#8F4300"
PRIMARY_LIGHT = "#FFE3CC"
BG = "#FFF7EE"               # fondo crema
CARD = "#FFFFFF"
TEXT = "#3B2A1E"             # marrón oscuro
MUTED = "#8A7566"
BORDER = "#EBCFB5"
STRIPE = "#FFF4E8"           # filas alternadas
SELECT = "#FFCF9E"           # fila seleccionada

# tipografia 
FONT_FAMILY = "Segoe UI"
FONT = (FONT_FAMILY, 10)
FONT_BOLD = (FONT_FAMILY, 10, "bold")
FONT_BIG = (FONT_FAMILY, 11)
FONT_TITLE = (FONT_FAMILY, 18, "bold")
FONT_H2 = (FONT_FAMILY, 14, "bold")
FONT_SMALL = (FONT_FAMILY, 9)

SYSTEM_NAME = "Soporte Técnico"
SYSTEM_SUBTITLE = "Sistema de tickets para electrodomésticos del hogar"


def apply_theme(root):
    root.configure(bg=BG)
    # fuente para los widgets que no son ttk (los ttk usan los estilos de abajo)
    root.option_add("*Text.font", FONT_BIG)
    root.option_add("*Listbox.font", FONT)
    root.option_add("*Toplevel.background", BG)
    root.option_add("*TCombobox*Listbox.background", CARD)
    root.option_add("*TCombobox*Listbox.foreground", TEXT)
    root.option_add("*TCombobox*Listbox.selectBackground", SELECT)
    root.option_add("*TCombobox*Listbox.selectForeground", TEXT)
    root.option_add("*TCombobox*Listbox.font", FONT)

    s = ttk.Style(root)
    s.theme_use("clam")                                  # tema que permite cambiar colores

    s.configure(".", background=BG, foreground=TEXT, font=FONT, bordercolor=BORDER,
                focuscolor=BG, troughcolor=BG)
    s.configure("TFrame", background=BG)
    s.configure("TLabel", background=BG, foreground=TEXT)
    s.configure("Muted.TLabel", foreground=MUTED)
    s.configure("Bold.TLabel", font=FONT_BOLD)
    s.configure("H2.TLabel", font=FONT_H2)

    # tarjetas (fondo blanco con borde suave)
    s.configure("Card.TFrame", background=CARD, relief="solid", borderwidth=1, bordercolor=BORDER)
    s.configure("Card.TLabel", background=CARD, foreground=TEXT)
    s.configure("CardBold.TLabel", background=CARD, foreground=TEXT, font=FONT_BOLD)
    s.configure("CardMuted.TLabel", background=CARD, foreground=MUTED)
    s.configure("CardH2.TLabel", background=CARD, foreground=TEXT, font=FONT_H2)

    # encabezado naranja
    s.configure("Header.TFrame", background=PRIMARY)
    s.configure("Header.TLabel", background=PRIMARY, foreground="white", font=FONT_TITLE)
    s.configure("HeaderSub.TLabel", background=PRIMARY, foreground="#FFE7D1", font=FONT)

    # botones
    s.configure("TButton", background=PRIMARY_LIGHT, foreground=PRIMARY_DEEP, bordercolor="#F5C9A0",
                lightcolor=PRIMARY_LIGHT, darkcolor=PRIMARY_LIGHT, padding=(14, 7), font=FONT_BOLD, relief="flat")
    s.map("TButton",
          background=[("disabled", "#F3EBE3"), ("active", "#FFD2AE")],
          foreground=[("disabled", "#B9A999")],
          bordercolor=[("disabled", BORDER)],
          lightcolor=[("active", "#FFD2AE")], darkcolor=[("active", "#FFD2AE")])
    s.configure("Accent.TButton", background=PRIMARY, foreground="white", bordercolor=PRIMARY_DARK,
                lightcolor=PRIMARY, darkcolor=PRIMARY, padding=(16, 8))
    s.map("Accent.TButton",
          background=[("disabled", "#F5CFA9"), ("active", PRIMARY_DARK)],
          foreground=[("disabled", "white")],
          bordercolor=[("disabled", "#F5CFA9")])
    s.configure("Header.TButton", background=PRIMARY_DARK, foreground="white", bordercolor=PRIMARY_DARK,
                lightcolor=PRIMARY_DARK, darkcolor=PRIMARY_DARK, padding=(14, 7))
    s.map("Header.TButton", background=[("active", PRIMARY_DEEP)])

    # campos de texto y listas desplegables
    s.configure("TEntry", fieldbackground=CARD, foreground=TEXT, bordercolor=BORDER,
                lightcolor=BORDER, darkcolor=BORDER, padding=(8, 6), insertcolor=TEXT)
    s.map("TEntry", bordercolor=[("focus", PRIMARY)], lightcolor=[("focus", PRIMARY)],
          darkcolor=[("focus", PRIMARY)])
    s.configure("TCombobox", fieldbackground=CARD, background=PRIMARY_LIGHT, foreground=TEXT,
                bordercolor=BORDER, lightcolor=BORDER, darkcolor=BORDER, arrowcolor=PRIMARY_DARK,
                padding=(6, 5))
    s.map("TCombobox", fieldbackground=[("readonly", CARD)], foreground=[("readonly", TEXT)],
          selectbackground=[("readonly", CARD)], selectforeground=[("readonly", TEXT)],
          bordercolor=[("focus", PRIMARY)], background=[("active", PRIMARY_LIGHT)])

    # tablas
    s.configure("Treeview", background=CARD, fieldbackground=CARD, foreground=TEXT,
                rowheight=32, bordercolor=BORDER, lightcolor=BORDER, darkcolor=BORDER, font=FONT_BIG)
    s.map("Treeview", background=[("selected", SELECT)], foreground=[("selected", TEXT)])
    s.configure("Treeview.Heading", background=PRIMARY_LIGHT, foreground=PRIMARY_DEEP, font=FONT_BOLD,
                relief="flat", padding=(8, 8), bordercolor=BORDER)
    s.map("Treeview.Heading", background=[("active", "#FFD2AE")])

    # pestañas
    s.configure("TNotebook", background=BG, borderwidth=0, tabmargins=(0, 4, 0, 0))
    s.configure("TNotebook.Tab", background="#F6E3D0", foreground=PRIMARY_DEEP, padding=(22, 9),
                font=FONT_BOLD, borderwidth=0)
    s.map("TNotebook.Tab", background=[("selected", PRIMARY), ("active", PRIMARY_LIGHT)],
          foreground=[("selected", "white")],
          padding=[("selected", (22, 9)), ("!selected", (22, 9))],      # todas las pestañas del mismo tamaño
          expand=[("selected", (0, 0, 0, 0))])

    # barras de desplazamiento
    s.configure("Vertical.TScrollbar", background="#F2C9A3", troughcolor=BG, bordercolor=BG,
                arrowcolor=PRIMARY_DEEP, lightcolor="#F2C9A3", darkcolor="#F2C9A3")
    s.map("Vertical.TScrollbar", background=[("active", PRIMARY)])

    s.configure("TSeparator", background=BORDER)


def style_text(widget):
    # aplica el estilo a un tk.Text (que no es ttk)
    widget.configure(bg=CARD, fg=TEXT, relief="flat", font=FONT_BIG, padx=10, pady=8,
                     highlightthickness=1, highlightbackground=BORDER, highlightcolor=PRIMARY,
                     insertbackground=TEXT, selectbackground=SELECT, selectforeground=TEXT)


def center(window, width, height):
    # tamaño fijo y centrada en la pantalla
    x = max((window.winfo_screenwidth() - width) // 2, 0)
    y = max((window.winfo_screenheight() - height) // 2 - 20, 0)
    window.geometry(f"{width}x{height}+{x}+{y}")


def make_header(parent, title, subtitle="", buttons=()):
    # franja naranja de arriba. buttons: lista de (texto, comando) que van a la derecha.
    # Devuelve (frame, label_titulo, label_subtitulo)
    frame = ttk.Frame(parent, style="Header.TFrame", padding=(28, 16))
    frame.pack(fill="x")
    left = ttk.Frame(frame, style="Header.TFrame")
    left.pack(side="left")
    lbl_title = ttk.Label(left, text=title, style="Header.TLabel")
    lbl_title.pack(anchor="w")
    lbl_subtitle = ttk.Label(left, text=subtitle, style="HeaderSub.TLabel")
    lbl_subtitle.pack(anchor="w")
    for text, command in buttons:
        ttk.Button(frame, text=text, command=command, style="Header.TButton").pack(side="right", padx=(8, 0))
    return frame, lbl_title, lbl_subtitle
