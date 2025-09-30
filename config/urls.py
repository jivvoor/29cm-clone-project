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
        description="""
        # ShopSite API Documentation
        
        Django 기반 이커머스 플랫폼 API 문서입니다.
        
        ## 주요 기능
        - 상품 관리 및 검색
        - 사용자 인증 (소셜 로그인 지원)
        - 장바구니 관리
        - 주문 및 결제
        - Q&A 및 리뷰 시스템
        
        ## 인증
        - 소셜 로그인: Google, Naver, Kakao
        - JWT 토큰 기반 인증
        
        ## 결제
        - 포트원(Portone) PG 연동
        """,
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@shopsite.local"),
        license=openapi.License(name="MIT License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
    patterns=[
        path('shop/', include('shop.urls')),
        path('users/', include('users.urls')),
        path('cart/', include('cart.urls')),
        path('review/', include('review.urls')),
        path('qna/', include('qna.urls')),
    ],
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
