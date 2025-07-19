from django.urls import path
from . import views

app_name = 'review'

urlpatterns = [
    path('create/<int:product_id>/', views.create_review, name='create_review'),
    # 내 리뷰 리스트 등 추가 가능
]