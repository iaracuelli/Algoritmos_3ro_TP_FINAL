from managers.product_manager import ProductManager
from models.product import Product
from models.product_category import ProductCategory
import pytest 

def test_create_product():
    manager = ProductManager()
    category = ProductCategory(1, "Electro")
    product = manager.create_product("Heladera", category)
    assert product in manager.products
    assert product.name == "Heladera"
    assert product.category == category


def test_create_duplicate_product():
    manager = ProductManager()
    category = ProductCategory(1, "Electro")
    product = manager.create_product("Heladera", category)
    with pytest.raises(Exception):
        manager.create_product("Heladera", category)