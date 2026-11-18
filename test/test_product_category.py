from models.product_category import ProductCategory

def test_create_product_category():
    productCategory = ProductCategory(1, "Electro")
    assert productCategory.id == 1
    assert productCategory.name == "Electro"
    