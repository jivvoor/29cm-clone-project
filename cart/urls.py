from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from .api import CartViewSet, CartItemViewSet

app_name = 'cart'

# API Router
router = DefaultRouter()
router.register(r'api/cart', CartViewSet, basename='cart')
router.register(r'api/cart-items', CartItemViewSet, basename='cart-item')

urlpatterns = [
    # API URLs
    path('', include(router.urls)),
    
    # Web URLs
    path('add/<int:product_id>/', views.add_cart, name='add_cart'),
    path('minus/<int:product_id>/', views.minus_cart, name='minus_cart'),
    path('delete_selected_items/', views.delete_selected_items, name='delete_selected_items'),
    path('delete_item/', views.delete_item, name='delete_item'),
    path('update_quantity/', views.update_quantity, name='update_quantity'),
    path('', views.cart_detail, name='cart_detail'),
]