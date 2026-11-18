# utils/console.py
# Utilidades para mejorar la salida por consola

def separador(titulo=None):
    print("\n" + "=" * 40)
    if titulo:
        print(titulo)
        print("=" * 40)
    print()

def linea():
    print("-" * 40)
