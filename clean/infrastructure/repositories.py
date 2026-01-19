from domain.entities import Book, Cart, CartItem, Customer
from interfaces.repositories import BookRepositoryInterface, CartRepositoryInterface, CustomerRepositoryInterface
from .db_models.models import BookModel, CartModel, CartItemModel, CustomerModel
from django.db import transaction

# Adapter cho Kho Sách
class DjangoBookRepository(BookRepositoryInterface):
    def get_by_id(self, book_id: int) -> Book:
        try:
            # 1. Lấy dữ liệu từ Django ORM
            orm_book = BookModel.objects.get(id=book_id)
            
            # 2. Chuyển đổi thành Entity Domain (Use Case chỉ hiểu cái này)
            return Book(
                id=orm_book.id,
                title=orm_book.title,
                author=orm_book.author,
                price=float(orm_book.price),
                stock=orm_book.stock
            )
        except BookModel.DoesNotExist: 
            return None

# Adapter cho Kho Giỏ hàng
class DjangoCartRepository(CartRepositoryInterface):
    def get_by_customer_id(self, customer_id: int) -> Cart:
        # Tìm hoặc tạo mới CartModel trong DB, liên kết với CustomerModel
        orm_cart, _ = CartModel.objects.get_or_create(customer_id=customer_id)
        
        # Chuyển đổi các items của Django sang items của Domain
        domain_items = []
        for item in orm_cart.items.all():
            domain_book = Book(
                id=item.book.id,
                title=item.book.title,
                author=item.book.author,
                price=float(item.book.price),
                stock=item.book.stock
            )
            domain_items.append(CartItem(book=domain_book, quantity=item.quantity))
            
        return Cart(
            id=orm_cart.id,
            customer_id=orm_cart.customer_id,
            items=domain_items,
            created_at=orm_cart.created_at
        )

    @transaction.atomic
    def save(self, cart: Cart):
        # Lưu từ Domain Entity ngược trở lại Database
        # 1. Lấy Cart Model, liên kết với CustomerModel
        orm_cart, _ = CartModel.objects.get_or_create(customer_id=cart.customer_id)
        
        # 2. Xóa hết items cũ, lưu lại items mới (cách đơn giản nhất)
        orm_cart.items.all().delete()
        
        for item in cart.items:
            orm_book = BookModel.objects.get(id=item.book.id)
            CartItemModel.objects.create(
                cart=orm_cart,
                book=orm_book,
                quantity=item.quantity
            )

# Adapter cho Kho Khách hàng
class DjangoCustomerRepository(CustomerRepositoryInterface):
    def get_by_email(self, email: str) -> Customer | None:
        try:
            # 1. Lấy dữ liệu từ Django ORM
            orm_customer = CustomerModel.objects.get(email=email)
            
            # 2. Chuyển đổi thành Entity Domain
            return Customer(
                id=orm_customer.id,
                name=orm_customer.username, # Ánh xạ username -> name
                email=orm_customer.email,
                password=orm_customer.password # Mật khẩu đã được băm
            )
        except CustomerModel.DoesNotExist:
            return None

    def save(self, customer: Customer) -> Customer:
        # Dùng create_user để tự động băm mật khẩu
        orm_customer = CustomerModel.objects.create_user(
            username=customer.name,
            email=customer.email,
            password=customer.password
        )
        # Trả về entity domain của customer vừa được tạo
        return Customer(
            id=orm_customer.id,
            name=orm_customer.username,
            email=orm_customer.email,
            password=orm_customer.password # Mật khẩu đã được băm
        )