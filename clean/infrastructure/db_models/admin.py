from django.contrib import admin
from .models import BookModel, CartModel, CartItemModel

# Register your models here.
admin.site.register(BookModel)
admin.site.register(CartModel)
admin.site.register(CartItemModel)
