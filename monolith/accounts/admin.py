from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Customer

# Dùng UserAdmin mặc định để quản lý Customer cho chuyên nghiệp
admin.site.register(Customer, UserAdmin)