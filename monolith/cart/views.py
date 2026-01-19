from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from books.models import Book
from .models import Cart, CartItem

@login_required # Bắt buộc phải đăng nhập mới được mua
def add_to_cart(request, book_id):
    # 1. Lấy thông tin quyển sách
    book = get_object_or_404(Book, id=book_id)
    
    # 2. Lấy giỏ hàng của user (nếu chưa có thì tạo mới)
    cart, created = Cart.objects.get_or_create(customer=request.user)
    
    # 3. Kiểm tra xem sách này đã có trong giỏ chưa
    cart_item, item_created = CartItem.objects.get_or_create(cart=cart, book=book)
    
    if not item_created:
        # Nếu đã có rồi thì tăng số lượng lên 1
        cart_item.quantity += 1
        cart_item.save()
    
    # 4. Quay lại trang danh sách sách để mua tiếp
    return redirect('book_list')
    
@login_required
def cart_detail(request):
    # Lấy giỏ hàng của user hiện tại
    cart, created = Cart.objects.get_or_create(customer=request.user)
    
    # Truyền giỏ hàng sang template
    return render(request, 'cart_detail.html', {'cart': cart})