from models.customer import Customer

def test_crear_customer():
    customer = Customer(1, "Ana", "ana@mail.com", "1234")
    assert customer.id == 1
    assert customer.name == "Ana"
    assert customer.email == "ana@mail.com"
    assert customer.password == "1234"


def test_login_correcto():
    customer = Customer(1, "Ana", "ana@mail.com", "1234")
    assert customer.login("1234") == True

def test_login_incorrecto():
    customer = Customer(1, "Ana", "ana@mail.com", "1234")
    assert customer.login("12345") == False