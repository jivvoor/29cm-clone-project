from django.core.management.base import BaseCommand
from django.core.files import File
from django.core.files.temp import NamedTemporaryFile
from shop.models import Product, Category, ColorCategory, SizeCategory
from users.models import User
import json
import requests
from urllib.parse import urlparse
import os

class Command(BaseCommand):
    help = 'JSON 파일에서 상품 데이터를 가져와서 데이터베이스에 저장합니다.'

    def add_arguments(self, parser):
        parser.add_argument('json_file', type=str, help='JSON 파일 경로')
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='실제로 데이터를 저장하지 않고 테스트만 실행',
        )

    def handle(self, *args, **options):
        json_file_path = options['json_file']
        dry_run = options['dry_run']

        if not os.path.exists(json_file_path):
            self.stdout.write(
                self.style.ERROR(f'JSON 파일을 찾을 수 없습니다: {json_file_path}')
            )
            return

        try:
            with open(json_file_path, 'r', encoding='utf-8') as file:
                products_data = json.load(file)
        except json.JSONDecodeError as e:
            self.stdout.write(
                self.style.ERROR(f'JSON 파일 형식 오류: {e}')
            )
            return

        self.stdout.write(
            self.style.SUCCESS(f'총 {len(products_data)}개의 상품 데이터를 처리합니다...')
        )

        # 기본 사용자 가져오기
        default_user = User.objects.first()
        if not default_user:
            default_user = User.objects.create_user(
                username='admin',
                email='admin@example.com',
                password='admin123'
            )
            self.stdout.write('기본 사용자 생성: admin')

        success_count = 0
        error_count = 0

        for i, product_data in enumerate(products_data, 1):
            try:
                self.stdout.write(f'처리 중... ({i}/{len(products_data)}) {product_data.get("name", "Unknown")}')

                if dry_run:
                    self.stdout.write(f'[DRY RUN] 상품 생성: {product_data.get("name")}')
                    success_count += 1
                    continue

                # 필수 필드 확인
                if not product_data.get('name'):
                    self.stdout.write(
                        self.style.WARNING(f'상품명이 없습니다. 건너뜁니다.')
                    )
                    error_count += 1
                    continue

                # 중복 상품 확인
                if Product.objects.filter(name=product_data['name']).exists():
                    self.stdout.write(
                        self.style.WARNING(f'이미 존재하는 상품입니다: {product_data["name"]}')
                    )
                    continue

                # 브랜드(작성자) 처리: brand → User(username=brand)
                brand_name = product_data.get('brand')
                if brand_name:
                    user, _ = User.objects.get_or_create(
                        username=brand_name,
                        defaults={
                            'email': f'{brand_name}@example.com',
                            'password': User.objects.make_random_password()
                        }
                    )
                else:
                    user = default_user

                # category, color, size는 None 또는 기본값
                category = None
                color = None
                size = None

                # 가격 처리
                try:
                    price = int(product_data.get('price', 0))
                    if price <= 0:
                        price = 10000
                except (ValueError, TypeError):
                    price = 10000

                # 재고 처리
                stock = 10

                # 상품 생성
                product = Product.objects.create(
                    name=product_data['name'],
                    price=price,
                    category=category,
                    color=color,
                    size=size,
                    host=user,
                    stock=stock,
                    status='a'
                )

                # 이미지 처리: image_url → head_image
                image_url = product_data.get('image_url')
                if image_url:
                    try:
                        headers = {
                            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
                        }
                        response = requests.get(image_url, headers=headers, timeout=10)
                        response.raise_for_status()

                        parsed_url = urlparse(image_url)
                        file_extension = os.path.splitext(parsed_url.path)[1] or '.jpg'

                        temp_file = NamedTemporaryFile(delete=False, suffix=file_extension)
                        temp_file.write(response.content)
                        temp_file.flush()

                        django_file = File(temp_file, name=f"{product.name}{file_extension}")
                        product.head_image.save(f"{product.name}{file_extension}", django_file, save=True)
                        self.stdout.write(f'이미지 저장 완료: {product.name}')
                    except Exception as e:
                        self.stdout.write(
                            self.style.WARNING(f'이미지 다운로드 실패 ({image_url}): {e}')
                        )

                success_count += 1
                self.stdout.write(
                    self.style.SUCCESS(f'상품 생성 완료: {product.name}')
                )

            except Exception as e:
                error_count += 1
                self.stdout.write(
                    self.style.ERROR(f'상품 생성 실패: {e}')
                )
                continue

        self.stdout.write(
            self.style.SUCCESS(f'\n=== 처리 완료 ===')
        )
        self.stdout.write(f'성공: {success_count}개')
        self.stdout.write(f'실패: {error_count}개')
        self.stdout.write(f'총 처리: {len(products_data)}개') 