# Dự án Môn học Kiến trúc và Thiết kế Phần mềm

## Tổng quan

Đây là dự án môn học Kiến trúc và Thiết kế Phần mềm, được xây dựng với 3 phiên bản khác nhau:

*   **khai_project1_monolithic:** Phiên bản ứng dụng nguyên khối (Monolithic) truyền thống sử dụng Django.
*   **khai_project1_clean_arch:** Phiên bản ứng dụng theo kiến trúc sạch (Clean Architecture).
*   **khai_project1_microservices:** Phiên bản ứng dụng sử dụng kiến trúc Microservices, bao gồm 3 dịch vụ riêng biệt:
    *   **Book Service:** Quản lý thông tin sách (Cổng 8000).
    *   **Customer Service:** Quản lý thông tin người dùng (Cổng 8001).
    *   **Cart Service:** Quản lý giỏ hàng (Cổng 8002).

## Yêu cầu

*   Python 3.x
*   MySQL
*   pip

## Cài đặt

Để cài đặt các thư viện cần thiết, hãy chạy lệnh sau trong thư mục gốc của mỗi phiên bản:

```bash
pip install -r requirements.txt
```

## Cài đặt Cơ sở dữ liệu

Trước khi chạy ứng dụng, bạn cần tạo các cơ sở dữ liệu tương ứng trong MySQL.

```sql
CREATE DATABASE khai_bookstore;
CREATE DATABASE khai_bookstore_clean;
CREATE DATABASE ms_book_db;
CREATE DATABASE ms_cart_db;
CREATE DATABASE ms_customer_db;
```

## Hướng dẫn Chạy

### Phiên bản A: Monolithic

1.  Di chuyển vào thư mục `monolith`.
2.  Áp dụng các thay đổi vào cơ sở dữ liệu:
    ```bash
    python manage.py migrate
    ```
3.  Chạy ứng dụng:
    ```bash
    python manage.py runserver
    ```
    Ứng dụng sẽ chạy tại `http://localhost:8000/`.

### Phiên bản B: Clean Architecture

1.  Di chuyển vào thư mục `clean`.
2.  Áp dụng các thay đổi vào cơ sở dữ liệu:
    ```bash
    python manage.py migrate
    ```
3.  Chạy ứng dụng:
    ```bash
    python manage.py runserver
    ```
    Ứng dụng sẽ chạy tại `http://localhost:8000/`.

### Phiên bản C: Microservices

Để chạy phiên bản này, bạn cần mở 3 cửa sổ dòng lệnh (terminal) riêng biệt và chạy các lệnh sau cho mỗi dịch vụ.

**Terminal 1: Book Service**

```bash
cd micro/book_service
python manage.py migrate
python manage.py runserver 8000
```

**Terminal 2: Customer Service**

```bash
cd micro/customer_service
python manage.py migrate
python manage.py runserver 8001
```

**Terminal 3: Cart Service**

```bash
cd micro/cart_service
python manage.py migrate
python manage.py runserver 8002
```

## Kiểm thử API

Dưới đây là một số điểm cuối API để bạn có thể kiểm thử:

*   **Lấy thông tin giỏ hàng của khách hàng 1:** `http://localhost:8002/api/cart/1/`
*   **Lấy danh sách tất cả sách:** `http://localhost:8000/api/books/`
*   **Lấy thông tin chi tiết của sách có ID 1:** `http://localhost:8000/api/books/1/`
*   **Đăng ký người dùng mới:** `http://localhost:8001/api/register/` (POST)
*   **Đăng nhập:** `http://localhost:8001/api/login/` (POST)
