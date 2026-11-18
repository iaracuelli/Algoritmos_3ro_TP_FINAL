# persistence/productRepository.py
# Contrato para persistencia de productos y rubros (categorias de producto).
# Incluye una implementación en memoria (la usa ProductManager si no recibe repositorio).

from abc import ABC, abstractmethod

class ProductRepository(ABC):

    @abstractmethod
    def save(self, product):
        """Guarda un producto y devuelve el producto con su ID asignado."""
        pass

    @abstractmethod
    def list(self):
        """Devuelve la lista de todos los productos."""
        pass

    @abstractmethod
    def get_by_id(self, id):
        """Devuelve un producto según su ID o None si no existe."""
        pass

    @abstractmethod
    def save_category(self, category):
        """Guarda un rubro y devuelve el rubro con su ID asignado."""
        pass

    @abstractmethod
    def list_categories(self):
        """Devuelve la lista de todos los rubros."""
        pass


class ProductRepositoryMemory(ProductRepository):
    def __init__(self):
        self.products = []
        self.categories = []
        self._next_id = 1
        self._next_category_id = 1

    def save(self, product):
        product.id = self._next_id
        self._next_id += 1
        self.products.append(product)
        return product

    def list(self):
        return self.products

    def get_by_id(self, id):
        for product in self.products:
            if product.id == id:
                return product
        return None

    def save_category(self, category):
        category.id = self._next_category_id
        self._next_category_id += 1
        self.categories.append(category)
        return category

    def list_categories(self):
        return self.categories
