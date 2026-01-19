from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser

# Model Sách (Dùng để tạo bảng trong DB)
class BookModel(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField()

    class Meta:
        db_table = 'books'  # Đặt tên bảng rõ ràng

# Model for Customer, extending Django's built-in User
class CustomerModel(AbstractUser):
    # AbstractUser already has: username, first_name, last_name, email, password, etc.
    # We will use the `username` field to store the customer's name.
    # You can add more fields here if needed in the future.
    
    class Meta:
        db_table = 'customers'

# Model Giỏ hàng
class CartModel(models.Model):
    customer = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE,
        default=None, 
        null=True # Allow null for now, or assign a default user
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'carts'

# Model Chi tiết giỏ hàng
class CartItemModel(models.Model):
    cart = models.ForeignKey(CartModel, on_delete=models.CASCADE, related_name='items')
    book = models.ForeignKey(BookModel, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    class Meta:
        db_table = 'cart_items'