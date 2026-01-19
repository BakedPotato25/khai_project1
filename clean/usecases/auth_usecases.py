from domain.entities import Customer
from interfaces.repositories import CustomerRepositoryInterface

class RegisterCustomerUseCase:
    def __init__(self, customer_repository: CustomerRepositoryInterface):
        self.customer_repository = customer_repository

    def execute(self, name, email, password) -> Customer:
        # Business Rule: Check if customer already exists
        if self.customer_repository.get_by_email(email):
            raise ValueError(f"Customer with email {email} already exists.")
        
        # Create a domain entity
        new_customer = Customer(id=None, name=name, email=email, password=password)
        
        # Persist using the repository (password will be hashed here)
        created_customer = self.customer_repository.save(new_customer)
        
        return created_customer
