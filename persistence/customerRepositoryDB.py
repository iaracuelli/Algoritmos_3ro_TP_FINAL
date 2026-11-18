# persistence/customer_repositoryDB.py
# Implementación concreta del repositorio de clientes usando SQLite.
# Esta clase cumple el contrato CustomerRepository.

import sqlite3
from models.customer import Customer

class CustomerRepositoryDB:
    def __init__(self, db_path="customers.db"):          
        self.conn = sqlite3.connect(db_path)
        self._create_table()                            

    def _create_table(self):                              
        cursor = self.conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS customers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT NOT NULL,
                password TEXT NOT NULL,
                active INTEGER NOT NULL DEFAULT 1
            )
        """)
        self.conn.commit()

    def save(self, customer):                    
        cursor = self.conn.cursor()
        cursor.execute(
            "INSERT INTO customers (name, email, password, active) VALUES (?, ?, ?, ?)",
            (customer.name, customer.email, customer.password, int(customer.active))
        )
        self.conn.commit()
        customer.id = cursor.lastrowid               
        return customer   

    def update(self, customer):
        cursor = self.conn.cursor()
        cursor.execute(
            "UPDATE customers SET name = ?, email = ?, password = ?, active = ? WHERE id = ?",
            (customer.name, customer.email, customer.password, int(customer.active), customer.id)
        )
        self.conn.commit()
        return customer

    def _to_customer(self, row):
        id, name, email, password, active = row
        customer = Customer(id, name, email, password)
        customer.active = bool(active)                  # SQLite guarda 0/1
        return customer
    
    def list(self):                               
        cursor = self.conn.cursor()
        cursor.execute("SELECT id, name, email, password, active FROM customers")
        rows = cursor.fetchall()

        return [self._to_customer(row) for row in rows] # Se convierten las filas en objetos Customer
    
    def get_by_id(self, id,):              
        cursor = self.conn.cursor()
        cursor.execute(
            "SELECT id, name, email, password, active FROM customers WHERE id = ?",
            (id,)
        )
        row = cursor.fetchone()

        if row:                            
            return self._to_customer(row)
        return None
