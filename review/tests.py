from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from shop.models import Product, Category, SubCategory, SizeCategory, ColorCategory
from .models import Review

User = get_user_model()


class ReviewModelTest(TestCase):
    def setUp(self):
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
        self.size = SizeCategory.objects.create(name='M')
        self.color = ColorCategory.objects.create(name='빨강')

    def test_review_creation(self):
        """리뷰 생성 테스트"""
        review = Review.objects.create(
            user=self.user,
            product=self.product,
            rating=5,
            title='좋은 상품입니다',
            content='정말 만족스러운 구매였습니다.',
            size=self.size,
            color=self.color
        )
        
        self.assertEqual(review.user, self.user)
        self.assertEqual(review.product, self.product)
        self.assertEqual(review.rating, 5)
        self.assertEqual(review.title, '좋은 상품입니다')
        self.assertEqual(review.size, self.size)
        self.assertEqual(review.color, self.color)

    def test_review_str_method(self):
        """리뷰 __str__ 메서드 테스트"""
        review = Review.objects.create(
            user=self.user,
            product=self.product,
            rating=4,
            title='테스트 리뷰',
            content='테스트 내용'
        )
        expected_str = f"{self.user.email} - {self.product.name} - {review.title}"
        self.assertEqual(str(review), expected_str)

    def test_review_rating_validation(self):
        """리뷰 평점 유효성 검사 테스트"""
        # 유효한 평점 (1-5)
        review = Review.objects.create(
            user=self.user,
            product=self.product,
            rating=3,
            title='보통 상품',
            content='보통입니다'
        )
        self.assertEqual(review.rating, 3)

    def test_review_ordering(self):
        """리뷰 정렬 테스트"""
        review1 = Review.objects.create(
            user=self.user,
            product=self.product,
            rating=5,
            title='첫 번째 리뷰',
            content='첫 번째 내용'
        )
        
        review2 = Review.objects.create(
            user=self.user,
            product=self.product,
            rating=4,
            title='두 번째 리뷰',
            content='두 번째 내용'
        )
        
        reviews = Review.objects.all()
        # 최신순으로 정렬되는지 확인 (created_at 기준 내림차순)
        self.assertEqual(reviews[0], review2)
        self.assertEqual(reviews[1], review1)


class ReviewViewTest(TestCase):
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
        self.size = SizeCategory.objects.create(name='M')
        self.color = ColorCategory.objects.create(name='빨강')

    def test_review_list_view(self):
        """리뷰 목록 뷰 테스트"""
        Review.objects.create(
            user=self.user,
            product=self.product,
            rating=5,
            title='테스트 리뷰',
            content='테스트 내용',
            size=self.size,
            color=self.color
        )
        
        response = self.client.get(reverse('review:review_list', args=[self.product.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '테스트 리뷰')

    def test_review_create_view_authenticated(self):
        """로그인한 사용자의 리뷰 작성 뷰 테스트"""
        self.client.login(email='test@example.com', password='testpass123')
        
        response = self.client.get(reverse('review:review_create', args=[self.product.id]))
        self.assertEqual(response.status_code, 200)

    def test_review_create_view_unauthenticated(self):
        """비로그인 사용자의 리뷰 작성 뷰 테스트"""
        response = self.client.get(reverse('review:review_create', args=[self.product.id]))
        self.assertEqual(response.status_code, 302)  # 로그인 페이지로 리다이렉트

    def test_review_create_success(self):
        """리뷰 작성 성공 테스트"""
        self.client.login(email='test@example.com', password='testpass123')
        
        response = self.client.post(reverse('review:review_create', args=[self.product.id]), {
            'rating': 5,
            'title': '새로운 리뷰',
            'content': '새로운 리뷰 내용입니다',
            'size': self.size.id,
            'color': self.color.id
        })
        
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Review.objects.filter(
            user=self.user,
            product=self.product,
            title='새로운 리뷰'
        ).exists())

    def test_review_update_view(self):
        """리뷰 수정 뷰 테스트"""
        self.client.login(email='test@example.com', password='testpass123')
        
        review = Review.objects.create(
            user=self.user,
            product=self.product,
            rating=3,
            title='기존 리뷰',
            content='기존 내용',
            size=self.size,
            color=self.color
        )
        
        response = self.client.get(reverse('review:review_update', args=[review.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '기존 리뷰')

    def test_review_update_success(self):
        """리뷰 수정 성공 테스트"""
        self.client.login(email='test@example.com', password='testpass123')
        
        review = Review.objects.create(
            user=self.user,
            product=self.product,
            rating=3,
            title='기존 리뷰',
            content='기존 내용',
            size=self.size,
            color=self.color
        )
        
        response = self.client.post(reverse('review:review_update', args=[review.id]), {
            'rating': 5,
            'title': '수정된 리뷰',
            'content': '수정된 내용',
            'size': self.size.id,
            'color': self.color.id
        })
        
        self.assertEqual(response.status_code, 302)
        review.refresh_from_db()
        self.assertEqual(review.title, '수정된 리뷰')
        self.assertEqual(review.rating, 5)

    def test_review_delete_view(self):
        """리뷰 삭제 테스트"""
        self.client.login(email='test@example.com', password='testpass123')
        
        review = Review.objects.create(
            user=self.user,
            product=self.product,
            rating=3,
            title='삭제할 리뷰',
            content='삭제할 내용',
            size=self.size,
            color=self.color
        )
        
        response = self.client.post(reverse('review:review_delete', args=[review.id]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Review.objects.filter(id=review.id).exists())

    def test_review_access_control(self):
        """리뷰 접근 권한 테스트"""
        other_user = User.objects.create_user(
            email='other@example.com',
            password='testpass123'
        )
        
        review = Review.objects.create(
            user=other_user,
            product=self.product,
            rating=3,
            title='다른 사용자 리뷰',
            content='다른 사용자 내용',
            size=self.size,
            color=self.color
        )
        
        self.client.login(email='test@example.com', password='testpass123')
        
        # 다른 사용자의 리뷰 수정 시도
        response = self.client.get(reverse('review:review_update', args=[review.id]))
        self.assertEqual(response.status_code, 403)
        
        # 다른 사용자의 리뷰 삭제 시도
        response = self.client.post(reverse('review:review_delete', args=[review.id]))
        self.assertEqual(response.status_code, 403)