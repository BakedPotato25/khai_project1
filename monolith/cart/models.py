from django.db import models
from django.conf import settings # Để lấy model Customer đang dùng
from books.models import Book

class Cart(models.Model):
    # Cart: id, customer id, created at [cite: 11]
    customer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Cart of {self.customer.username}"
    # [THÊM ĐOẠN NÀY] Hàm tính tổng tiền cả giỏ hàng
    @property
    def total_price(self):
        # Lấy tất cả items trong giỏ, tính tổng tiền từng cái rồi cộng lại
        return sum(item.total_price for item in self.cartitem_set.all())

class CartItem(models.Model):
    # CartItem: id, cart_id, book_id, quantity [cite: 11]
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} x {self.book.title}"
    # [THÊM ĐOẠN NÀY] Hàm tính tiền cho từng dòng (Giá x Số lượng)
    @property
    def total_price(self):
        return self.book.price * self.quantity