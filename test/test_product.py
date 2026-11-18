from models.product import Product
from models.product_category import ProductCategory


def test_create_product():
    category = ProductCategory(1, "Electro")
    product = Product(1, "Heladera", category)
    assert product.id == 1
    assert product.name == "Heladera"
    assert product.category == category