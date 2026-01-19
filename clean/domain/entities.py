from dataclasses import dataclass, field
from typing import List, Optional
from datetime import datetime

# Định nghĩa Sách
@dataclass
class Book:
    id: int
    title: str
    author: str
    price: float
    stock: int

# Định nghĩa Khách hàng (User)
@dataclass
class Customer:
    id: int
    name: str
    email: str
    password: str

# Định nghĩa từng món trong giỏ (Cart Item)
@dataclass
class CartItem:
    book: Book
    quantity: int = 1

    @property
    def total_price(self) -> float:
        return self.book.price * self.quantity

# Định nghĩa Giỏ hàng
@dataclass
class Cart:
    id: int
    customer_id: int
    items: List[CartItem] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.now)

    def add_item(self, book: Book):
        # Logic: Nếu sách đã có trong giỏ thì tăng số lượng
        for item in self.items:
            if item.book.id == book.id:
                item.quantity += 1
                return
        # Nếu chưa có thì thêm mới
        new_item = CartItem(book=book, quantity=1)
        self.items.append(new_item)

    @property
    def total_price(self) -> float:
        return sum(item.total_price for item in self.items)