from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Customer

class CustomerRegistrationForm(UserCreationForm):
    # Kế thừa form tạo user sẵn có của Django, chỉ trỏ nó về model Customer của mình
    class Meta:
        model = Customer
        fields = ['username', 'email', 'name'] # Các trường cho phép user nhập