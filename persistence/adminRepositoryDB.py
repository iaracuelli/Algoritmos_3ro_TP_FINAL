# persistence/admin_repositoryDB.py
# Implementación concreta del repositorio de admin usando SQLite.
# Esta clase cumple el contrato AdminRepository.

import sqlite3
from models.admin import Admin

class AdminRepositoryDB:
    def __init__(self, db_path="admin.db"):          
        self.conn = sqlite3.connect(db_path)
        self._create_table()                            

    def _create_table(self):                              
        cursor = self.conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS admin (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT NOT NULL,
                password TEXT NOT NULL
            )
        """)
        self.conn.commit()

    def save(self, admin):                    
        cursor = self.conn.cursor()
        cursor.execute(
            "INSERT INTO admin (name, email, password) VALUES (?, ?, ?)",
            (admin.name, admin.email, admin.password)
        )
        self.conn.commit()
        admin.id = cursor.lastrowid               
        return admin 
    

    def list(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT id, name, email, password FROM admin")
        rows = cursor.fetchall()
        return [Admin(id, name, email, password) for id, name, email, password in rows]

    def get_by_id(self, id):
        cursor = self.conn.cursor()
        cursor.execute(
            "SELECT id, name, email, password FROM admin WHERE id = ?",
            (id,)
        )
        row = cursor.fetchone()
        if row:
            return Admin(*row)
        return None