from abc import ABC, abstractmethod
from typing import Optional
from domain.entities import Book, Cart, Customer

# Đây là Interface cho kho chứa Sách
class BookRepositoryInterface(ABC):
    @abstractmethod
    def get_by_id(self, book_id: int) -> Optional[Book]:
        pass

# Đây là Interface cho kho chứa Giỏ hàng
class CartRepositoryInterface(ABC):
    @abstractmethod
    def get_by_customer_id(self, customer_id: int) -> Cart:
        pass

    @abstractmethod
    def save(self, cart: Cart):
        pass

# Interface for Customer repository
class CustomerRepositoryInterface(ABC):
    @abstractmethod
    def get_by_email(self, email: str) -> Optional[Customer]:
        pass

    @abstractmethod
    def save(self, customer: Customer) -> Customer:
        pass