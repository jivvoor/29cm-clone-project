"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from shop import views as shop_views
from qna import views
from users import views

# drf-yasg for API docs
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="ShopSite API",
        default_version='v1',
        description="API documentation for ShopSite backend",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('', include('core.urls', namespace="core")),
    path("shop/", include('shop.urls', namespace="shop")),
    path('admin/', admin.site.urls),
    path("users/", include('users.urls', namespace="users")),
    path("accounts/", include("allauth.urls")),
    path("category/<category_slug>/", shop_views.ProductListByCategory.as_view(), name="product_category"),
    path('cart/', include('cart.urls')),
    path("qna/", include('qna.urls')),
    path('shopping_info/', views.shopping_info, name='shopping_info'),
    path('review/', include('review.urls')),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]  
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
