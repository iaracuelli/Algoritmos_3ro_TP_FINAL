# persistence/productRepositoryDB.py
# Implementación concreta del repositorio de productos y rubros usando SQLite.
# Esta clase cumple el contrato ProductRepository.

import sqlite3
from models.product import Product
from models.product_category import ProductCategory

class ProductRepositoryDB:
    def __init__(self, db_path="products.db"):
        self.conn = sqlite3.connect(db_path)
        self._create_tables()

    def _create_tables(self):
        cursor = self.conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS product_categories (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS products (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                category_id INTEGER
            )
        """)
        self.conn.commit()

    def save_category(self, category):
        cursor = self.conn.cursor()
        cursor.execute("INSERT INTO product_categories (name) VALUES (?)", (category.name,))
        self.conn.commit()
        category.id = cursor.lastrowid
        return category

    def list_categories(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT id, name FROM product_categories")
        return [ProductCategory(id, name) for id, name in cursor.fetchall()]

    def save(self, product):
        if product.category is not None and product.category.id is None:
            self.save_category(product.category)            # si el rubro es nuevo, se guarda primero
        category_id = product.category.id if product.category else None
        cursor = self.conn.cursor()
        cursor.execute(
            "INSERT INTO products (name, category_id) VALUES (?, ?)",
            (product.name, category_id)
        )
        self.conn.commit()
        product.id = cursor.lastrowid
        return product

    def _to_product(self, row):
        id, name, category_id, category_name = row
        category = ProductCategory(category_id, category_name) if category_id is not None else None
        return Product(id, name, category)

    def list(self):
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT p.id, p.name, c.id, c.name
            FROM products p LEFT JOIN product_categories c ON p.category_id = c.id
        """)
        return [self._to_product(row) for row in cursor.fetchall()]

    def get_by_id(self, id):
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT p.id, p.name, c.id, c.name
            FROM products p LEFT JOIN product_categories c ON p.category_id = c.id
            WHERE p.id = ?
        """, (id,))
        row = cursor.fetchone()
        if row:
            return self._to_product(row)
        return None
