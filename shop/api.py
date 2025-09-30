from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q
from .models import Category, SubCategory, NestedSubCategory, Product, SizeCategory, ColorCategory
from .serializers import (
    CategorySerializer, SubCategorySerializer, NestedSubCategorySerializer,
    ProductSerializer, ProductListSerializer, SizeCategorySerializer, ColorCategorySerializer
)

class CategoryViewSet(viewsets.ModelViewSet):
    """
    카테고리 API
    
    - list: 모든 카테고리 목록 조회
    - retrieve: 특정 카테고리 상세 조회
    - create: 새 카테고리 생성 (관리자만)
    - update: 카테고리 수정 (관리자만)
    - destroy: 카테고리 삭제 (관리자만)
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name']
    ordering_fields = ['name', 'id']
    ordering = ['name']

    @action(detail=True, methods=['get'])
    def products(self, request, pk=None):
        """특정 카테고리의 상품 목록 조회"""
        category = self.get_object()
        products = Product.objects.filter(category=category)
        
        # 필터링
        search = request.query_params.get('search', None)
        if search:
            products = products.filter(name__icontains=search)
        
        # 정렬
        ordering = request.query_params.get('ordering', None)
        if ordering:
            products = products.order_by(ordering)
        
        serializer = ProductListSerializer(products, many=True)
        return Response(serializer.data)

class SubCategoryViewSet(viewsets.ModelViewSet):
    """
    서브카테고리 API
    
    - list: 모든 서브카테고리 목록 조회
    - retrieve: 특정 서브카테고리 상세 조회
    """
    queryset = SubCategory.objects.all()
    serializer_class = SubCategorySerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category']
    search_fields = ['name']
    ordering_fields = ['name', 'id']
    ordering = ['name']

class NestedSubCategoryViewSet(viewsets.ModelViewSet):
    """
    중첩 서브카테고리 API
    """
    queryset = NestedSubCategory.objects.all()
    serializer_class = NestedSubCategorySerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['subcategory']

class ProductViewSet(viewsets.ModelViewSet):
    """
    상품 API
    
    - list: 상품 목록 조회 (검색, 필터링 지원)
    - retrieve: 상품 상세 조회
    - create: 새 상품 생성 (관리자만)
    - update: 상품 수정 (관리자만)
    - destroy: 상품 삭제 (관리자만)
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category', 'subcategory', 'nested_subcategory']
    search_fields = ['name', 'description']
    ordering_fields = ['name', 'price', 'created_at']
    ordering = ['-created_at']

    def get_serializer_class(self):
        if self.action == 'list':
            return ProductListSerializer
        return ProductSerializer

    @action(detail=False, methods=['get'])
    def featured(self, request):
        """추천 상품 목록 조회"""
        featured_products = self.get_queryset()[:10]  # 최근 상품 10개
        serializer = ProductListSerializer(featured_products, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def search(self, request):
        """상품 검색"""
        query = request.query_params.get('q', '')
        if query:
            products = self.get_queryset().filter(
                Q(name__icontains=query) | 
                Q(description__icontains=query)
            )
        else:
            products = self.get_queryset()
        
        serializer = ProductListSerializer(products, many=True)
        return Response(serializer.data)

class SizeCategoryViewSet(viewsets.ReadOnlyModelViewSet):
    """
    사이즈 카테고리 API (읽기 전용)
    """
    queryset = SizeCategory.objects.all()
    serializer_class = SizeCategorySerializer
    ordering = ['name']

class ColorCategoryViewSet(viewsets.ReadOnlyModelViewSet):
    """
    색상 카테고리 API (읽기 전용)
    """
    queryset = ColorCategory.objects.all()
    serializer_class = ColorCategorySerializer
    ordering = ['name']
