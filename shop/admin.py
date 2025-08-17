from django.contrib import admin
from django import forms
from . import models
from .models import Category, Product, SubCategory, NestedSubCategory, ProductDetailImage
from ckeditor_uploader.widgets import CKEditorUploadingWidget

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # SubCategory가 선택된 경우에만 필터링

@admin.register(models.ColorCategory)
class ColorCategoryAdmin(admin.ModelAdmin):
    pass

@admin.register(models.SizeCategory)
class SizeCategoryAdmin(admin.ModelAdmin):
    pass

@admin.register(models.Category)
class CategoryAdmin(admin.ModelAdmin):
    pass

@admin.register(models.NestedSubCategory)
class NestedSubCategoryAdmin(admin.ModelAdmin):
    pass

class NestedSubCategoryInline(admin.TabularInline):
    model = NestedSubCategory
    extra = 1

class ProductDetailImageInline(admin.TabularInline):
    model = ProductDetailImage
    extra = 1
    fields = ['image', 'order']
    ordering = ['order']

@admin.register(models.SubCategory)
class SubCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'slug']
    list_filter = ['category']
    inlines = [NestedSubCategoryInline]


@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    form = ProductForm
    list_display = ['name', 'nested_subcategory', 'price', 'stock']
    inlines = [ProductDetailImageInline]

# Register your models here.


