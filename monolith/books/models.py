from django.db import models

class Book(models.Model):
    # Book: id, title, author, price, stock [cite: 11]
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2) # Giá tiền
    stock = models.IntegerField() # Số lượng tồn kho

    def __str__(self):
        return self.title