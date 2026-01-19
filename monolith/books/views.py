from django.shortcuts import render
from .models import Book

def book_list(request):
    # Lấy tất cả sách từ database
    books = Book.objects.all()
    return render(request, 'book_list.html', {'books': books})