from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from django.shortcuts import get_object_or_404
from django.db.models import Q
from .models import Cart, CartItem
from .serializers import CartSerializer, CartItemSerializer
from shop.models import Product, SizeCategory, ColorCategory

class CartViewSet(viewsets.ModelViewSet):
    """
    장바구니 API
    
    - retrieve: 현재 사용자의 장바구니 조회
    - add_item: 장바구니에 상품 추가
    - remove_item: 장바구니에서 상품 제거
    - update_quantity: 상품 수량 업데이트
    - clear: 장바구니 비우기
    """
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication, SessionAuthentication]
    
    def get_queryset(self):
        # Swagger 스키마 생성 시 문제 방지
        if getattr(self, 'swagger_fake_view', False):
            return Cart.objects.none()
        
        # 인증된 사용자만 처리
        if self.request.user.is_authenticated:
            return Cart.objects.filter(user=self.request.user)
        return Cart.objects.none()
    
    def get_object(self):
        cart, created = Cart.objects.get_or_create(user=self.request.user)
        return cart
    
    @action(detail=False, methods=['post'])
    def add_item(self, request):
        """장바구니에 상품 추가"""
        product_id = request.data.get('product_id')
        quantity = int(request.data.get('quantity', 1))
        size_id = request.data.get('size_id')
        color_id = request.data.get('color_id')
        
        if not product_id:
            return Response({'error': 'product_id is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        product = get_object_or_404(Product, id=product_id)
        cart = self.get_object()
        
        # 사이즈와 색상 가져오기
        size = None
        color = None
        if size_id:
            size = get_object_or_404(SizeCategory, id=size_id)
        if color_id:
            color = get_object_or_404(ColorCategory, id=color_id)
        
        # 기존 아이템이 있는지 확인
        cart_item, created = CartItem.objects.get_or_create(
            cart=cart,
            product=product,
            size=size,
            color=color,
            defaults={'quantity': 0}
        )
        
        cart_item.quantity += quantity
        cart_item.save()
        
        serializer = CartItemSerializer(cart_item)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    @action(detail=False, methods=['post'])
    def remove_item(self, request):
        """장바구니에서 상품 제거"""
        cart_item_id = request.data.get('cart_item_id')
        
        if not cart_item_id:
            return Response({'error': 'cart_item_id is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        cart_item = get_object_or_404(
            CartItem,
            id=cart_item_id,
            cart__user=request.user
        )
        
        cart_item.delete()
        return Response({'message': 'Item removed successfully'}, status=status.HTTP_200_OK)
    
    @action(detail=False, methods=['post'])
    def update_quantity(self, request):
        """상품 수량 업데이트"""
        cart_item_id = request.data.get('cart_item_id')
        quantity = int(request.data.get('quantity', 1))
        
        if not cart_item_id:
            return Response({'error': 'cart_item_id is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        if quantity <= 0:
            return Response({'error': 'Quantity must be greater than 0'}, status=status.HTTP_400_BAD_REQUEST)
        
        cart_item = get_object_or_404(
            CartItem,
            id=cart_item_id,
            cart__user=request.user
        )
        
        cart_item.quantity = quantity
        cart_item.save()
        
        serializer = CartItemSerializer(cart_item)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @action(detail=False, methods=['post'])
    def clear(self, request):
        """장바구니 비우기"""
        cart = self.get_object()
        CartItem.objects.filter(cart=cart).delete()
        return Response({'message': 'Cart cleared successfully'}, status=status.HTTP_200_OK)

class CartItemViewSet(viewsets.ModelViewSet):
    """
    장바구니 아이템 API
    """
    serializer_class = CartItemSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication, SessionAuthentication]
    
    def get_queryset(self):
        # Swagger 스키마 생성 시 문제 방지
        if getattr(self, 'swagger_fake_view', False):
            return CartItem.objects.none()
        
        # 인증된 사용자만 처리
        if self.request.user.is_authenticated:
            return CartItem.objects.filter(cart__user=self.request.user, active=True)
        return CartItem.objects.none()
    
    def perform_create(self, serializer):
        cart, created = Cart.objects.get_or_create(user=self.request.user)
        serializer.save(cart=cart)
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)