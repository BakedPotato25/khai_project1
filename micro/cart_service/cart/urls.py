from django.urls import path
from .views import AddToCartView, CartDetailView

urlpatterns = [
    path('cart/add/', AddToCartView.as_view(), name='add-to-cart'),
    path('cart/<int:customer_id>/', CartDetailView.as_view(), name='cart-detail'),
]
