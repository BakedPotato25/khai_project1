from rest_framework import serializers
from .models import Cart, CartItem

class CartAddSerializer(serializers.Serializer):
    customer_id = serializers.IntegerField()
    book_id = serializers.IntegerField()
    quantity = serializers.IntegerField(min_value=1)

class CartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ('book_id', 'quantity')

class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)

    class Meta:
        model = Cart
        fields = ('id', 'customer_id', 'created_at', 'items')
