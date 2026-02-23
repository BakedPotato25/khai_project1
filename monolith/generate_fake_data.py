import os
import sys
import django
import random

# Set up Django environment
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'khai_project1.settings')
django.setup()

from books.models import Book
from accounts.models import Customer
from cart.models import Cart, CartItem
from faker import Faker

fake = Faker()

def generate_books(n=100):
    print(f"Generating {n} books...")
    books = []
    for _ in range(n):
        book = Book(
            title=fake.catch_phrase(),
            author=fake.name(),
            price=round(random.uniform(5.0, 100.0), 2),
            stock=random.randint(0, 200)
        )
        books.append(book)
    Book.objects.bulk_create(books)
    print("Books created.")

def generate_customers(n=50):
    print(f"Generating {n} customers...")
    customers = []
    for _ in range(n):
        username = fake.user_name()
        # handle unique constraint just in case
        while Customer.objects.filter(username=username).exists():
            username = fake.user_name()
            
        email = fake.email()
        while Customer.objects.filter(email=email).exists():
            email = fake.email()
            
        customer = Customer(
            username=username,
            name=fake.name(),
            email=email
        )
        customer.set_password('password123')
        customers.append(customer)
    Customer.objects.bulk_create(customers)
    print("Customers created.")

def generate_carts(n=30):
    print(f"Generating {n} carts...")
    customers = list(Customer.objects.all())
    books = list(Book.objects.all())
    
    if not customers or not books:
        print("Need customers and books to create carts.")
        return

    for _ in range(n):
        customer = random.choice(customers)
        cart = Cart.objects.create(customer=customer)
        
        # Add 1 to 5 random items
        num_items = random.randint(1, 5)
        for _ in range(num_items):
            book = random.choice(books)
            CartItem.objects.create(
                cart=cart,
                book=book,
                quantity=random.randint(1, 4)
            )
    print("Carts created.")

if __name__ == '__main__':
    print("Starting data generation...")
    # Optionally clear old data
    # Book.objects.all().delete()
    # Customer.objects.exclude(is_superuser=True).delete()
    # Cart.objects.all().delete()
    
    generate_books(100)
    generate_customers(50)
    generate_carts(30)
    print("Data generation complete!")
