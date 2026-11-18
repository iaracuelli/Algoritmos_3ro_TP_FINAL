# gui/dialogs.py
# Formulario genérico: muestra campos, y al aceptar llama a on_submit(valores).
# Si on_submit lanza una Exception, se muestra el error y el formulario queda abierto.

import tkinter as tk
from tkinter import ttk, messagebox
from gui.theme import style_text, center, make_header


def ask_form(parent, title, fields, on_submit, submit_text="Aceptar"):
    # fields: lista de (etiqueta, clave, tipo, [opciones], [valor por defecto])
    # tipos: "entry", "password", "text", "combo", "combo_free"
    dlg = tk.Toplevel(parent)
    dlg.title(title)
    dlg.transient(parent)
    dlg.resizable(False, False)

    make_header(dlg, title)

    frame = ttk.Frame(dlg, padding=(28, 20))
    frame.pack(fill="both", expand=True)

    widgets = {}
    for field in fields:
        label, key, kind = field[0], field[1], field[2]
        options = field[3] if len(field) > 3 else []
        default = field[4] if len(field) > 4 else None

        ttk.Label(frame, text=label, style="Bold.TLabel").pack(anchor="w", pady=(0, 3))
        if kind == "entry":
            widget = ttk.Entry(frame, width=48)
        elif kind == "password":
            widget = ttk.Entry(frame, width=48, show="*")
        elif kind == "text":
            widget = tk.Text(frame, width=48, height=6, wrap="word")
            style_text(widget)
        else:
            state = "readonly" if kind == "combo" else "normal"
            widget = ttk.Combobox(frame, values=options, state=state, width=45)
            if default in options:
                widget.set(default)
            elif options and kind == "combo":
                widget.current(0)
        widget.pack(fill="x", pady=(0, 12))
        widgets[key] = (kind, widget)

    def read(kind, widget):
        if kind == "text":
            return widget.get("1.0", "end").strip()
        return widget.get().strip()

    def submit():
        values = {key: read(kind, widget) for key, (kind, widget) in widgets.items()}
        try:
            on_submit(values)
        except Exception as e:
            messagebox.showerror("Error", str(e), parent=dlg)
            return
        dlg.destroy()

    buttons = ttk.Frame(frame)
    buttons.pack(fill="x", pady=(6, 0))
    ttk.Button(buttons, text=submit_text, command=submit, style="Accent.TButton").pack(side="right")
    ttk.Button(buttons, text="Cancelar", command=dlg.destroy).pack(side="right", padx=8)

    dlg.update_idletasks()
    center(dlg, max(dlg.winfo_reqwidth(), 520), dlg.winfo_reqheight())
    dlg.grab_set()
    first = next(iter(widgets.values()))[1]
    first.focus_set()
    return dlg
