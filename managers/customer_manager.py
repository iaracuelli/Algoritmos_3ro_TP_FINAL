from models.customer import Customer


class CustomerManager:
    def __init__(self, repository):
        self.repository = repository                    


    def create_customer(self, name, email, password):
            for customer in self.repository.list():
                if customer.email == email:
                    raise Exception("Ya existe un cliente con ese email")
            
            customer = Customer(
                id=None,
                name=name,
                email=email,
                password=password   
            )
            return self.repository.save(customer)
        

    def list_customers(self):
        return self.repository.list()
        

    def get_customer_by_id(self, id):
            return self.repository.get_by_id(id)

    def update_customer(self, customer):
            return self.repository.update(customer)
