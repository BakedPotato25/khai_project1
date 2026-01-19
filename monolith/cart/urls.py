from django.urls import path
from . import views

urlpatterns = [
    # Đường dẫn xem chi tiết giỏ hàng (http://127.0.0.1:8000/cart/)
    path('', views.cart_detail, name='cart_detail'),
    # Đường dẫn sẽ có dạng: /cart/add/5/ (Thêm sách có id=5 vào giỏ)
    path('add/<int:book_id>/', views.add_to_cart, name='add_to_cart'),
]