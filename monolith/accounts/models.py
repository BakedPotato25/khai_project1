from django.db import models
from django.contrib.auth.models import AbstractUser

# Customer: id, name, email, password (kế thừa từ AbstractUser để có sẵn login)
class Customer(AbstractUser):
    # AbstractUser đã có sẵn username, password, email.
    # Chúng ta thêm các trường đề bài yêu cầu nếu thiếu.
    # Ở đây dùng 'name' thay vì first_name/last_name cho giống đề
    name = models.CharField(max_length=255)
    
    # Cấu hình để đăng nhập bằng email (tùy chọn, cho chuyên nghiệp)
    email = models.EmailField(unique=True)
    
    def __str__(self):
        return self.username