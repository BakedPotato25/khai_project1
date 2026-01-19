from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from .forms import CustomerRegistrationForm

def register(request):
    if request.method == 'POST':
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user) # Đăng ký xong tự đăng nhập luôn
            return redirect('book_list') # Chuyển hướng về trang danh sách sách
    else:
        form = CustomerRegistrationForm()
    return render(request, 'registration/register.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('book_list') # Đăng xuất xong quay về xem sách