import requests
from django.conf import settings
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Cart, CartItem
from .serializers import CartSerializer, CartAddSerializer

class AddToCartView(generics.GenericAPIView):
    serializer_class = CartAddSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        customer_id = serializer.validated_data['customer_id']
        book_id = serializer.validated_data['book_id']
        quantity = serializer.validated_data['quantity']

        cart, _ = Cart.objects.get_or_create(customer_id=customer_id)
        cart_item, created = CartItem.objects.get_or_create(cart=cart, book_id=book_id)

        if not created:
            cart_item.quantity += quantity
        else:
            cart_item.quantity = quantity
        
        cart_item.save()

        # Return the full cart state after adding the item
        response_serializer = CartSerializer(cart)
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)


class CartDetailView(APIView):
    def get(self, request, customer_id, *args, **kwargs):
        try:
            cart = Cart.objects.get(customer_id=customer_id)
        except Cart.DoesNotExist:
            return Response({"error": "Cart not found"}, status=status.HTTP_404_NOT_FOUND)

        cart_items = cart.items.all()
        total_price = 0
        response_data = []

        for item in cart_items:
            try:
                # Server-to-server API call to Book Service
                book_service_url = f"{settings.BOOK_SERVICE_URL}{item.book_id}/"
                response = requests.get(book_service_url)
                response.raise_for_status() 
                book_data = response.json()
                
                item_total = float(book_data.get('price', 0)) * item.quantity
                total_price += item_total

                response_data.append({
                    'book_id': item.book_id,
                    'title': book_data.get('title'),
                    'price': book_data.get('price'),
                    'quantity': item.quantity,
                    'item_total': item_total,
                })

            except requests.exceptions.RequestException as e:
                # Handle cases where the book service is down or the book is not found
                response_data.append({
                    'book_id': item.book_id,
                    'title': 'Book details not available',
                    'price': 'N/A',
                    'quantity': item.quantity,
                    'item_total': 0,
                    'error': str(e),
                })

        return Response({
            'cart_items': response_data,
            'total_price': total_price
        })
