from models.product import Product
from models.product_category import ProductCategory
from persistence.productRepository import ProductRepositoryMemory


class ProductManager:
    # Si no recibe repositorio guarda en memoria (como antes); con repositorio guarda en SQLite
    def __init__(self, repository=None):
        self.repository = repository if repository is not None else ProductRepositoryMemory()

    @property
    def products(self):
        return self.list_products()


    def create_product(self, name, category):
            for product in self.repository.list():
                if product.name == name:
                    raise Exception("Ya existe un producto con ese nombre")
            
            product = Product(
                id=None,
                name=name,
                category=category  
            )
            return self.repository.save(product)
        

    def list_products(self):
        return self.repository.list()
        

    def get_product_by_id(self, id):
       return self.repository.get_by_id(id)

    def create_category(self, name):
        for category in self.repository.list_categories():
            if category.name == name:
                raise Exception("Ya existe un rubro con ese nombre")
        return self.repository.save_category(ProductCategory(None, name))

    def list_categories(self):
        return self.repository.list_categories()
