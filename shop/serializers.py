from rest_framework import serializers
from .models import Category, SubCategory, NestedSubCategory, Product, SizeCategory, ColorCategory

class CategorySerializer(serializers.ModelSerializer):
    subcategories = serializers.SerializerMethodField()
    
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'subcategories']
    
    def get_subcategories(self, obj):
        subcategories = obj.subcategory_set.all()
        return SubCategorySerializer(subcategories, many=True).data

class SubCategorySerializer(serializers.ModelSerializer):
    nested_subcategories = serializers.SerializerMethodField()
    
    class Meta:
        model = SubCategory
        fields = ['id', 'category', 'name', 'slug', 'nested_subcategories']
    
    def get_nested_subcategories(self, obj):
        nested_subcategories = obj.nested_subcategories.all()  # related_name 사용
        return NestedSubCategorySerializer(nested_subcategories, many=True).data

class NestedSubCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = NestedSubCategory
        fields = ['id', 'parent_subcategory', 'name', 'slug']  # 실제 필드명으로 수정

class SizeCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SizeCategory
        fields = ['id', 'name']

class ColorCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ColorCategory
        fields = ['id', 'name']

class ProductSerializer(serializers.ModelSerializer):
    nested_subcategory_name = serializers.CharField(source='nested_subcategory.name', read_only=True)
    
    class Meta:
        model = Product
        fields = [
            'id', 'name', 'price', 'description', 'image', 'head_image',
            'status', 'stock', 'host',
            'nested_subcategory', 'nested_subcategory_name',
            'colors', 'sizes',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']

class ProductListSerializer(serializers.ModelSerializer):
    """상품 목록용 간소화된 시리얼라이저"""
    category_name = serializers.CharField(source='category.name', read_only=True)
    subcategory_name = serializers.CharField(source='subcategory.name', read_only=True)
    
    class Meta:
        model = Product
        fields = [
            'id', 'name', 'price', 'image',
            'category_name', 'subcategory_name'
        ]