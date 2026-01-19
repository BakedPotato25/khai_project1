from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from infrastructure.repositories import DjangoBookRepository, DjangoCartRepository, DjangoCustomerRepository
from usecases.cart_usecases import AddBookToCartUseCase, GetCartUseCase
from usecases.auth_usecases import RegisterCustomerUseCase
from infrastructure.db_models.models import BookModel

# View 1: Hiển thị danh sách sách
def index(request):
    # Để đơn giản cho việc hiển thị, ta có thể gọi Model trực tiếp (CQRS pattern)
    # Hoặc chuẩn chỉ thì viết thêm GetBooksUseCase (nhưng thế hơi dài dòng cho bài tập)
    books = BookModel.objects.all()
    return render(request, 'clean_book_list.html', {'books': books})

# View 2: Xử lý thêm vào giỏ (QUAN TRỌNG)
@login_required
def add_to_cart(request, book_id):
    # 1. Chuẩn bị các Adapter (Repo)
    book_repo = DjangoBookRepository()
    cart_repo = DjangoCartRepository()

    # 2. Khởi tạo Use Case và bơm dependencies vào
    use_case = AddBookToCartUseCase(book_repo, cart_repo)

    # 3. Thực thi Logic
    customer_id = request.user.id
    
    try:
        use_case.execute(customer_id, book_id)
        print("Đã gọi Use Case thành công!")
    except Exception as e:
        print(f"Lỗi: {e}")

    return redirect('index')

# View 3: Đăng ký
def register(request):
    if request.method == 'POST':
        # 1. Khởi tạo dependencies
        customer_repo = DjangoCustomerRepository()
        use_case = RegisterCustomerUseCase(customer_repository=customer_repo)
        
        # 2. Lấy dữ liệu từ form
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            # 3. Thực thi use case
            use_case.execute(name=username, email=email, password=password)
            # 4. Khi thành công, chuyển đến trang đăng nhập
            return redirect('login')
        except ValueError as e:
            # 5. Nếu thất bại (VD: user đã tồn tại), hiển thị lỗi
            return render(request, 'registration/register.html', {'error': str(e)})
            
    # Nếu là request GET, chỉ hiển thị form
    return render(request, 'registration/register.html')

# View 4: Chi tiết giỏ hàng
@login_required
def cart_detail(request):
    # 1. Khởi tạo dependencies
    cart_repo = DjangoCartRepository()
    use_case = GetCartUseCase(cart_repo=cart_repo)
    
    # 2. Lấy ID khách hàng từ user đã đăng nhập
    customer_id = request.user.id
    
    # 3. Thực thi use case để lấy cart entity
    cart = use_case.execute(customer_id)
    
    # 4. Render template với dữ liệu cart
    return render(request, 'cart_detail.html', {'cart': cart})