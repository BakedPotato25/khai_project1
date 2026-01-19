from domain.entities import Book, Cart
from interfaces.repositories import BookRepositoryInterface, CartRepositoryInterface

class AddBookToCartUseCase:
    # Use Case cần 2 cái kho để làm việc: Kho sách và Kho giỏ hàng
    def __init__(self, book_repo: BookRepositoryInterface, cart_repo: CartRepositoryInterface):
        self.book_repo = book_repo
        self.cart_repo = cart_repo

    def execute(self, customer_id: int, book_id: int):
        # 1. Tìm quyển sách theo ID
        book = self.book_repo.get_by_id(book_id)
        if not book:
            raise Exception("Book not found")

        # 2. Lấy giỏ hàng của khách (nếu chưa có thì Repository tự lo việc tạo mới)
        cart = self.cart_repo.get_by_customer_id(customer_id)

        # 3. Thêm sách vào giỏ (Logic này nằm trong Entity Cart mình vừa viết)
        cart.add_item(book)

        # 4. Lưu giỏ hàng đã cập nhật xuống database
        self.cart_repo.save(cart)
        
        print(f"Success! Added '{book.title}' to cart.") # Log nhẹ để biết chạy ngon

class GetCartUseCase:
    def __init__(self, cart_repo: CartRepositoryInterface):
        self.cart_repo = cart_repo

    def execute(self, customer_id: int) -> Cart:
        # Logic nghiệp vụ đơn giản: chỉ cần lấy giỏ hàng cho người dùng.
        # Repository xử lý việc tạo nếu nó không tồn tại.
        # Domain entity xử lý việc tính tổng giá.
        cart = self.cart_repo.get_by_customer_id(customer_id)
        return cart