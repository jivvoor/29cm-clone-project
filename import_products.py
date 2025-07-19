#!/usr/bin/env python
"""
상품 데이터 JSON 파일을 Django 모델로 안전하게 변환하는 스크립트
"""

import os
import sys
import django
import json
from pathlib import Path

# Django 설정
sys.path.append(str(Path(__file__).parent))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from shop.models import Product, Category, ColorCategory, SizeCategory
from users.models import User
from django.core.files import File
from django.core.files.temp import NamedTemporaryFile
import requests
from urllib.parse import urlparse

def download_image(image_url, product_name):
    """이미지 URL에서 파일을 다운로드하여 Django File 객체로 반환"""
    try:
        response = requests.get(image_url, timeout=10)
        response.raise_for_status()
        
        # 파일 확장자 추출
        parsed_url = urlparse(image_url)
        file_extension = os.path.splitext(parsed_url.path)[1] or '.jpg'
        
        # 임시 파일 생성
        temp_file = NamedTemporaryFile(delete=False, suffix=file_extension)
        temp_file.write(response.content)
        temp_file.flush()
        
        # Django File 객체 생성
        django_file = File(temp_file, name=f"{product_name}{file_extension}")
        return django_file
    except Exception as e:
        print(f"이미지 다운로드 실패 ({image_url}): {e}")
        return None

def get_or_create_category(category_name):
    """카테고리 가져오기 또는 생성"""
    if not category_name:
        return None
    
    category, created = Category.objects.get_or_create(
        name=category_name,
        defaults={'slug': category_name.lower().replace(' ', '-')}
    )
    if created:
        print(f"새 카테고리 생성: {category_name}")
    return category

def get_or_create_color(color_name):
    """색상 가져오기 또는 생성"""
    if not color_name:
        return None
    
    color, created = ColorCategory.objects.get_or_create(
        name=color_name,
        defaults={'slug': color_name.lower().replace(' ', '-')}
    )
    if created:
        print(f"새 색상 생성: {color_name}")
    return color

def get_or_create_size(size_name):
    """사이즈 가져오기 또는 생성"""
    if not size_name:
        return None
    
    size, created = SizeCategory.objects.get_or_create(
        name=size_name,
        defaults={'slug': size_name.lower().replace(' ', '-')}
    )
    if created:
        print(f"새 사이즈 생성: {size_name}")
    return size

def get_default_user():
    """기본 사용자 가져오기 (첫 번째 사용자 또는 생성)"""
    try:
        return User.objects.first()
    except:
        # 사용자가 없으면 기본 사용자 생성
        user = User.objects.create_user(
            username='admin',
            email='admin@example.com',
            password='admin123'
        )
        print("기본 사용자 생성: admin")
        return user

def import_products_from_json(json_file_path):
    """JSON 파일에서 상품 데이터를 가져와서 Django 모델로 변환"""
    
    try:
        with open(json_file_path, 'r', encoding='utf-8') as file:
            products_data = json.load(file)
    except FileNotFoundError:
        print(f"JSON 파일을 찾을 수 없습니다: {json_file_path}")
        return
    except json.JSONDecodeError as e:
        print(f"JSON 파일 형식 오류: {e}")
        return
    
    print(f"총 {len(products_data)}개의 상품 데이터를 처리합니다...")
    
    # 기본 사용자 가져오기
    default_user = get_default_user()
    
    success_count = 0
    error_count = 0
    
    for i, product_data in enumerate(products_data, 1):
        try:
            print(f"처리 중... ({i}/{len(products_data)}) {product_data.get('name', 'Unknown')}")
            
            # 필수 필드 확인
            if not product_data.get('name'):
                print(f"상품명이 없습니다. 건너뜁니다.")
                error_count += 1
                continue
            
            # 중복 상품 확인
            if Product.objects.filter(name=product_data['name']).exists():
                print(f"이미 존재하는 상품입니다: {product_data['name']}")
                continue
            
            # 카테고리 처리
            category = get_or_create_category(product_data.get('category'))
            
            # 색상 처리
            color = get_or_create_color(product_data.get('color'))
            
            # 사이즈 처리
            size = get_or_create_size(product_data.get('size'))
            
            # 가격 처리 (숫자가 아니면 기본값 사용)
            try:
                price = int(product_data.get('price', 0))
                if price <= 0:
                    price = 10000  # 기본 가격
            except (ValueError, TypeError):
                price = 10000
            
            # 재고 처리
            stock = int(product_data.get('stock', 10))
            
            # 상품 생성
            product = Product.objects.create(
                name=product_data['name'],
                price=price,
                category=category,
                color=color,
                size=size,
                host=default_user,
                stock=stock,
                status='a'  # 정상 상태
            )
            
            # 이미지 처리
            image_url = product_data.get('image_url')
            if image_url:
                django_file = download_image(image_url, product.name)
                if django_file:
                    product.head_image.save(f"{product.name}.jpg", django_file, save=True)
                    print(f"이미지 저장 완료: {product.name}")
            
            success_count += 1
            print(f"상품 생성 완료: {product.name}")
            
        except Exception as e:
            error_count += 1
            print(f"상품 생성 실패: {e}")
            continue
    
    print(f"\n=== 처리 완료 ===")
    print(f"성공: {success_count}개")
    print(f"실패: {error_count}개")
    print(f"총 처리: {len(products_data)}개")

if __name__ == "__main__":
    # JSON 파일 경로 설정
    json_file_path = "products.json"  # JSON 파일 경로를 여기에 입력하세요
    
    if not os.path.exists(json_file_path):
        print(f"JSON 파일이 없습니다: {json_file_path}")
        print("JSON 파일 경로를 확인하고 다시 실행하세요.")
        sys.exit(1)
    
    print("상품 데이터 가져오기를 시작합니다...")
    import_products_from_json(json_file_path) 