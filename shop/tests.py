from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from .models import Category, SubCategory, NestedSubCategory, Product, SizeCategory, ColorCategory

User = get_user_model()


class CategoryModelTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(
            name='테스트 카테고리',
            slug='test-category'
        )

    def test_category_creation(self):
        """카테고리 생성 테스트"""
        self.assertEqual(str(self.category), '테스트 카테고리')
        self.assertEqual(self.category.slug, 'test-category')

    def test_category_str_method(self):
        """카테고리 __str__ 메서드 테스트"""
        self.assertEqual(str(self.category), '테스트 카테고리')


class ProductModelTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(
            name='테스트 카테고리',
            slug='test-category'
        )
        self.subcategory = SubCategory.objects.create(
            name='테스트 서브카테고리',
            slug='test-subcategory',
            category=self.category
        )
        self.nested_subcategory = NestedSubCategory.objects.create(
            name='테스트 중첩서브카테고리',
            slug='test-nested-subcategory',
            subcategory=self.subcategory
        )
        self.size = SizeCategory.objects.create(name='M')
        self.color = ColorCategory.objects.create(name='빨강')

    def test_product_creation(self):
        """상품 생성 테스트"""
        product = Product.objects.create(
            name='테스트 상품',
            price=50000,
            description='테스트 상품 설명',
            category=self.category,
            subcategory=self.subcategory,
            nested_subcategory=self.nested_subcategory
        )
        
        self.assertEqual(product.name, '테스트 상품')
        self.assertEqual(product.price, 50000)
        self.assertEqual(product.category, self.category)
        self.assertEqual(product.subcategory, self.subcategory)
        self.assertEqual(product.nested_subcategory, self.nested_subcategory)

    def test_product_str_method(self):
        """상품 __str__ 메서드 테스트"""
        product = Product.objects.create(
            name='테스트 상품',
            price=50000,
            description='테스트 상품 설명',
            category=self.category,
            subcategory=self.subcategory
        )
        self.assertEqual(str(product), '테스트 상품')


class ProductViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            email='test@example.com',
            password='testpass123'
        )
        self.category = Category.objects.create(
            name='테스트 카테고리',
            slug='test-category'
        )
        self.subcategory = SubCategory.objects.create(
            name='테스트 서브카테고리',
            slug='test-subcategory',
            category=self.category
        )
        self.product = Product.objects.create(
            name='테스트 상품',
            price=50000,
            description='테스트 상품 설명',
            category=self.category,
            subcategory=self.subcategory
        )

    def test_home_view(self):
        """홈페이지 뷰 테스트"""
        response = self.client.get(reverse('shop:home'))
        self.assertEqual(response.status_code, 200)

    def test_product_detail_view(self):
        """상품 상세보기 뷰 테스트"""
        response = self.client.get(reverse('shop:product_detail', args=[self.product.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.product.name)
        self.assertContains(response, str(self.product.price))

    def test_product_list_by_category(self):
        """카테고리별 상품 목록 뷰 테스트"""
        response = self.client.get(reverse('shop:product_category', args=[self.category.slug]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.product.name)

    def test_product_list_by_subcategory(self):
        """서브카테고리별 상품 목록 뷰 테스트"""
        response = self.client.get(reverse('shop:product_subcategory', 
                                        args=[self.category.slug, self.subcategory.slug]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.product.name)

    def test_search_view(self):
        """검색 뷰 테스트"""
        response = self.client.get(reverse('shop:search'), {'q': '테스트'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.product.name)

    def test_search_empty_query(self):
        """빈 검색어로 검색 테스트"""
        response = self.client.get(reverse('shop:search'))
        self.assertEqual(response.status_code, 200)


class ProductAPITest(TestCase):
    def setUp(self):
        self.client = Client()
        self.category = Category.objects.create(
            name='테스트 카테고리',
            slug='test-category'
        )
        self.subcategory = SubCategory.objects.create(
            name='테스트 서브카테고리',
            slug='test-subcategory',
            category=self.category
        )

    def test_category_api_list(self):
        """카테고리 API 목록 테스트"""
        response = self.client.get('/shop/api/categories/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '테스트 카테고리')

    def test_subcategory_api_list(self):
        """서브카테고리 API 목록 테스트"""
        response = self.client.get('/shop/api/subcategories/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '테스트 서브카테고리')

    def test_category_api_detail(self):
        """카테고리 API 상세보기 테스트"""
        response = self.client.get(f'/shop/api/categories/{self.category.id}/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '테스트 카테고리')

    def test_subcategory_api_detail(self):
        """서브카테고리 API 상세보기 테스트"""
        response = self.client.get(f'/shop/api/subcategories/{self.subcategory.id}/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '테스트 서브카테고리')