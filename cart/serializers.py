from rest_framework import serializers
from .models import Cart, CartItem
from shop.serializers import ProductListSerializer, SizeCategorySerializer, ColorCategorySerializer

class CartItemSerializer(serializers.ModelSerializer):
    product = ProductListSerializer(read_only=True)
    product_id = serializers.IntegerField(write_only=True)
    size = SizeCategorySerializer(read_only=True)
    size_id = serializers.IntegerField(write_only=True, required=False)
    color = ColorCategorySerializer(read_only=True)
    color_id = serializers.IntegerField(write_only=True, required=False)
    sub_total = serializers.ReadOnlyField()
    
    class Meta:
        model = CartItem
        fields = [
            'id', 'product', 'product_id', 'quantity', 'active',
            'size', 'size_id', 'color', 'color_id', 'sub_total'
        ]

class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)
    total_items = serializers.SerializerMethodField()
    total_price = serializers.SerializerMethodField()
    
    class Meta:
        model = Cart
        fields = ['id', 'items', 'total_items', 'total_price', 'data_added']
        read_only_fields = ['data_added']
    
    def get_total_items(self, obj):
        return sum(item.quantity for item in obj.cartitem_set.filter(active=True))
    
    def get_total_price(self, obj):
        return sum(item.sub_total() for item in obj.cartitem_set.filter(active=True))
