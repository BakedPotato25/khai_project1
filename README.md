# So sánh các Kiến trúc Phần mềm: Monolith, Clean Architecture, và Microservices

Repository này chứa một ứng dụng web bán sách đơn giản được triển khai theo ba kiến trúc phần mềm khác nhau. Mục tiêu là để trình bày, so sánh và đối chiếu các cách tiếp cận này trong thực tế.

## Bối cảnh chung

Ứng dụng của chúng ta là một cửa hàng sách trực tuyến cơ bản, cho phép người dùng xem sách, quản lý giat hàng và tài khoản người dùng. Chức năng này được dùng làm nền tảng để triển khai 3 mô hình kiến trúc:

1.  **Monolith:** Một ứng dụng Django đơn khối truyền thống.
2.  **Clean Architecture:** Một ứng dụng Django được cấu trúc theo các nguyên tắc của Clean Architecture.
3.  **Microservices:** Một hệ thống gồm nhiều dịch vụ nhỏ giao tiếp với nhau.

---

## 1. Kiến trúc Monolithic (`/monolith`)

Đây là cách tiếp cận truyền thống và phổ biến nhất để xây dựng ứng dụng web, đặc biệt là trong giai đoạn đầu.

### a. Khái niệm

Kiến trúc Monolithic (đơn khối) cấu trúc một ứng dụng như một thể thống nhất duy nhất. Tất cả các thành phần, từ giao diện người dùng (UI), logic nghiệp vụ (business logic), đến lớp truy cập dữ liệu (data access layer), đều được xây dựng và triển khai cùng nhau như một đơn vị duy nhất.

### b. Cấu trúc dự án

Dự án này sử dụng cấu trúc Django tiêu chuẩn:

-   `khai_project1/`: Thư mục cấu hình chính của dự án Django.
-   `books/`, `cart/`, `accounts/`: Các "app" của Django, mỗi app chịu trách nhiệm cho một nhóm chức năng cụ thể.
-   `manage.py`: Công cụ dòng lệnh của Django.

### c. Ưu và Nhược điểm

**Ưu điểm:**
*   **Phát triển đơn giản:** Dễ dàng để bắt đầu, phát triển và gỡ lỗi vì mọi thứ đều ở cùng một nơi.
*   **Triển khai dễ dàng:** Chỉ cần triển khai một ứng dụng duy nhất lên máy chủ.
*   **Thử nghiệm (Testing):** Có thể thực hiện End-to-End testing một cách tương đối dễ dàng.

**Nhược điểm:**
*   **Khó bảo trì khi mở rộng:** Khi ứng dụng lớn dần, mã nguồn trở nên phức tạp và các thành phần phụ thuộc chặt chẽ vào nhau, gây khó khăn cho việc thay đổi hoặc thêm tính năng mới.
*   **Hạn chế về công nghệ:** Toàn bộ ứng dụng phải sử dụng chung một ngăn xếp công nghệ (technology stack).
*   **Rủi ro cao:** Một lỗi nhỏ trong một module có thể làm sập toàn bộ ứng dụng.
*   **Khó khăn trong việc áp dụng công nghệ mới:** Việc nâng cấp hoặc thay đổi một phần của công nghệ nền tảng là rất khó khăn và rủi ro.


### d. Cách chạy dự án

```bash
# Di chuyển vào thư mục dự án
cd monolith

# (Tùy chọn) Tạo môi trường ảo
# python -m venv venv
# source venv/bin/activate (trên Linux/macOS) hoặc venv\Scripts\activate (trên Windows)

# Cài đặt các thư viện cần thiết
pip install -r requirements.txt

# Chạy migrations để tạo cơ sở dữ liệu
python manage.py migrate

# (Tùy chọn) Tạo tài khoản quản trị
python manage.py createsuperuser

# Khởi động máy chủ phát triển
python manage.py runserver
```
Sau đó, truy cập vào `http://127.0.0.1:8000` trên trình duyệt của bạn.

---

## 2. Kiến trúc Clean Architecture (`/clean`)

Kiến trúc này tập trung vào việc tách biệt các mối quan tâm (separation of concerns) bằng cách tổ chức mã nguồn thành các lớp đồng tâm, độc lập.

### a. Khái niệm

Clean Architecture, hay còn gọi là Hexagonal Architecture hoặc Onion Architecture, nhấn mạnh **Quy tắc Phụ thuộc (The Dependency Rule)**: các lớp bên trong không được biết gì về các lớp bên ngoài. Điều này có nghĩa là logic nghiệp vụ cốt lõi và mô hình dữ liệu (domain) hoàn toàn độc lập với framework, cơ sở dữ liệu, hay giao diện người dùng.

-   **Entities (Domain):** Chứa các đối tượng nghiệp vụ cốt lõi và các quy tắc chung nhất.
-   **Use Cases:** Chứa logic nghiệp vụ cụ thể của ứng dụng, điều phối các Entities để hoàn thành một tác vụ.
-   **Interface Adapters:** Lớp chuyển đổi dữ liệu. Chứa các `Repositories`, `Presenters`, và `Controllers`.
-   **Frameworks & Drivers:** Lớp ngoài cùng, chứa các công cụ như web framework (Django), cơ sở dữ liệu (SQLite), UI...

### b. Cấu trúc dự án

-   `domain/`: Tương ứng với lớp **Entities**. Chứa các lớp Python thuần túy (POCOs) định nghĩa các đối tượng nghiệp vụ.
-   `usecases/`: Tương ứng với lớp **Use Cases**. Chứa logic chính của ứng dụng.
-   `interfaces/`: Định nghĩa các "cổng" (ports) trừu tượng, ví dụ như `BookRepository` interface. Các use case sẽ phụ thuộc vào các interface này, chứ không phải các class cụ thể.
-   `infrastructure/`: Tương ứng với **Frameworks & Drivers**. Đây là nơi triển khai cụ thể các interface.
    -   `db_models/`: Chứa các models của Django, triển khai chi tiết việc lưu trữ dữ liệu.
    -   `repositories.py`: Triển khai cụ thể `BookRepository` interface, sử dụng models của Django để tương tác với CSDL.
    -   `web_views/`: Chứa các view và URL của Django, xử lý các yêu cầu HTTP.

### c. Ưu và Nhược điểm

**Ưu điểm:**
*   **Độc lập với Framework/UI/CSDL:** Logic nghiệp vụ không phụ thuộc vào các yếu tố bên ngoài, giúp dễ dàng thay đổi chúng mà không ảnh hưởng đến nghiệp vụ.
*   **Khả năng kiểm thử (Testability):** Có thể kiểm thử logic nghiệp vụ và use case một cách độc lập mà không cần đến framework hay CSDL.
*   **Dễ bảo trì:** Cấu trúc rõ ràng, tách biệt giúp việc tìm kiếm, sửa lỗi và nâng cấp dễ dàng hơn.

**Nhược điểm:**
*   **Phức tạp ban đầu:** Cần nhiều thời gian hơn để thiết lập và có thể tạo ra nhiều tệp và lớp hơn cho các tác vụ đơn giản.
*   **Đòi hỏi kỷ luật:** Nhóm phát triển phải tuân thủ nghiêm ngặt các quy tắc phụ thuộc.

### d. Cách chạy dự án

Các bước tương tự như dự án Monolith:
```bash
cd clean
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

---

## 3. Kiến trúc Microservices (`/micro`)

Kiến trúc này cấu trúc ứng dụng thành một tập hợp các dịch vụ nhỏ, độc lập.

### a. Khái niệm

Trong kiến trúc Microservices, ứng dụng được chia thành các dịch vụ nhỏ, mỗi dịch vụ chạy trong tiến trình riêng và giao tiếp với nhau thông qua các cơ chế nhẹ như API HTTP. Mỗi dịch vụ được xây dựng xoay quanh một chức năng nghiệp vụ cụ thể.

Hệ thống này bao gồm các dịch vụ:
-   `customer_service`: Quản lý tài khoản người dùng và xác thực.
-   `book_service`: Quản lý thông tin sách.
-   `cart_service`: Quản lý giỏ hàng của người dùng.

### b. Cấu trúc dự án

Mỗi thư mục con trong `/micro` là một dự án Django hoàn chỉnh, hoạt động như một dịch vụ độc lập:
-   `micro/book_service/`
-   `micro/cart_service/`
-   `micro/customer_service/`

Mỗi dịch vụ có cơ sở dữ liệu riêng và không chia sẻ bất cứ điều gì với các dịch vụ khác ở cấp độ mã nguồn hay CSDL. Giao tiếp giữa các dịch vụ (nếu cần) sẽ được thực hiện qua các cuộc gọi API.

### c. Ưu và Nhược điểm

**Ưu điểm:**
*   **Độc lập và tự chủ:** Mỗi dịch vụ có thể được phát triển, triển khai, và mở rộng quy mô một cách độc lập.
*   **Linh hoạt về công nghệ:** Có thể sử dụng các ngăn xếp công nghệ khác nhau cho các dịch vụ khác nhau.
*   **Tăng khả năng chống lỗi:** Lỗi trong một dịch vụ không làm sập toàn bộ hệ thống (mặc dù có thể ảnh hưởng đến các chức năng liên quan).
*   **Phát triển song song:** Các nhóm khác nhau có thể làm việc trên các dịch vụ khác nhau cùng một lúc.

**Nhược điểm:**
*   **Phức tạp trong vận hành (Operational Complexity):** Đòi hỏi hệ thống triển khai, giám sát, và quản lý phức tạp hơn nhiều.
*   **Độ trễ mạng:** Giao tiếp giữa các dịch vụ qua mạng có thể gây ra độ trễ.
*   **Quản lý dữ liệu phân tán:** Đảm bảo tính nhất quán của dữ liệu trên nhiều dịch vụ là một thách thức lớn.
*   **Khó khăn trong gỡ lỗi:** Việc truy vết một yêu cầu qua nhiều dịch vụ để tìm lỗi có thể rất phức tạp.

### d. Cách chạy dự án

Mỗi dịch vụ phải được chạy trong một terminal riêng.

**Terminal 1: Chạy Customer Service**
```bash
cd micro/customer_service
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver 8001
```

**Terminal 2: Chạy Book Service**
```bash
cd micro/book_service
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver 8002
```

**Terminal 3: Chạy Cart Service**
```bash
cd micro/cart_service
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver 8003
```
Lưu ý rằng mỗi dịch vụ được chạy trên một cổng (port) khác nhau.

## Tổng kết

Việc lựa chọn kiến trúc nào phụ thuộc rất nhiều vào bối cảnh của dự án:

| Tiêu chí | Monolith | Clean Architecture | Microservices |
|---|---|---|---|
| **Tốc độ phát triển ban đầu** | Nhanh | Chậm hơn | Chậm |
| **Bảo trì dài hạn** | Khó | Dễ | Trung bình (phức tạp ở khía cạnh khác) |
| **Khả năng mở rộng** | Thấp (phải mở rộng toàn bộ) | Cao (logic) | Rất cao (độc lập từng dịch vụ) |
| **Độ phức tạp vận hành** | Thấp | Thấp | Cao |
| **Đội ngũ phù hợp** | Nhỏ, mới bắt đầu | Mọi quy mô, cần chất lượng cao | Lớn, có kinh nghiệm DevOps |

-   **Monolith** là lựa chọn tốt cho các dự án nhỏ, MVP (Minimum Viable Product), hoặc khi đội ngũ còn nhỏ và cần ra sản phẩm nhanh.
-   **Clean Architecture** là một sự đầu tư cho tương lai, phù hợp cho các ứng dụng phức tạp, có vòng đời dài, nơi khả năng bảo trì và linh hoạt là ưu tiên hàng đầu.
-   **Microservices** phù hợp với các hệ thống rất lớn, phức tạp, đòi hỏi khả năng mở rộng cực cao và được phát triển bởi nhiều đội ngũ khác nhau.