from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse
from shop.models import Product, Category, SubCategory
from .models import QnA

User = get_user_model()


class QnAModelTest(TestCase):
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

    def test_qna_creation(self):
        """Q&A 생성 테스트"""
        qna = QnA.objects.create(
            user=self.user,
            product=self.product,
            title='상품 문의드립니다',
            content='이 상품의 재고는 언제쯤 들어올까요?',
            is_public=True
        )
        
        self.assertEqual(qna.user, self.user)
        self.assertEqual(qna.product, self.product)
        self.assertEqual(qna.title, '상품 문의드립니다')
        self.assertTrue(qna.is_public)

    def test_qna_str_method(self):
        """Q&A __str__ 메서드 테스트"""
        qna = QnA.objects.create(
            user=self.user,
            product=self.product,
            title='테스트 Q&A',
            content='테스트 내용'
        )
        expected_str = f"{self.user.email} - {self.product.name} - {qna.title}"
        self.assertEqual(str(qna), expected_str)

    def test_qna_ordering(self):
        """Q&A 정렬 테스트"""
        qna1 = QnA.objects.create(
            user=self.user,
            product=self.product,
            title='첫 번째 Q&A',
            content='첫 번째 내용'
        )
        
        qna2 = QnA.objects.create(
            user=self.user,
            product=self.product,
            title='두 번째 Q&A',
            content='두 번째 내용'
        )
        
        qnas = QnA.objects.all()
        # 최신순으로 정렬되는지 확인 (created_at 기준 내림차순)
        self.assertEqual(qnas[0], qna2)
        self.assertEqual(qnas[1], qna1)

    def test_qna_public_private(self):
        """Q&A 공개/비공개 설정 테스트"""
        public_qna = QnA.objects.create(
            user=self.user,
            product=self.product,
            title='공개 Q&A',
            content='공개 내용',
            is_public=True
        )
        
        private_qna = QnA.objects.create(
            user=self.user,
            product=self.product,
            title='비공개 Q&A',
            content='비공개 내용',
            is_public=False
        )
        
        self.assertTrue(public_qna.is_public)
        self.assertFalse(private_qna.is_public)


class QnAViewTest(TestCase):
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

    def test_qna_list_view(self):
        """Q&A 목록 뷰 테스트"""
        QnA.objects.create(
            user=self.user,
            product=self.product,
            title='테스트 Q&A',
            content='테스트 내용',
            is_public=True
        )
        
        response = self.client.get(reverse('qna:qna_index', args=[self.product.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '테스트 Q&A')

    def test_qna_create_view_authenticated(self):
        """로그인한 사용자의 Q&A 작성 뷰 테스트"""
        self.client.login(email='test@example.com', password='testpass123')
        
        response = self.client.get(reverse('qna:qna_new', args=[self.product.id]))
        self.assertEqual(response.status_code, 200)

    def test_qna_create_view_unauthenticated(self):
        """비로그인 사용자의 Q&A 작성 뷰 테스트"""
        response = self.client.get(reverse('qna:qna_new', args=[self.product.id]))
        self.assertEqual(response.status_code, 302)  # 로그인 페이지로 리다이렉트

    def test_qna_create_success(self):
        """Q&A 작성 성공 테스트"""
        self.client.login(email='test@example.com', password='testpass123')
        
        response = self.client.post(reverse('qna:qna_new', args=[self.product.id]), {
            'title': '새로운 Q&A',
            'content': '새로운 Q&A 내용입니다',
            'is_public': True
        })
        
        self.assertEqual(response.status_code, 302)
        self.assertTrue(QnA.objects.filter(
            user=self.user,
            product=self.product,
            title='새로운 Q&A'
        ).exists())

    def test_qna_detail_view(self):
        """Q&A 상세보기 뷰 테스트"""
        qna = QnA.objects.create(
            user=self.user,
            product=self.product,
            title='테스트 Q&A',
            content='테스트 내용',
            is_public=True
        )
        
        response = self.client.get(reverse('qna:qna_detail', args=[qna.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '테스트 Q&A')

    def test_qna_edit_view(self):
        """Q&A 수정 뷰 테스트"""
        self.client.login(email='test@example.com', password='testpass123')
        
        qna = QnA.objects.create(
            user=self.user,
            product=self.product,
            title='기존 Q&A',
            content='기존 내용'
        )
        
        response = self.client.get(reverse('qna:qna_edit', args=[qna.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '기존 Q&A')

    def test_qna_edit_success(self):
        """Q&A 수정 성공 테스트"""
        self.client.login(email='test@example.com', password='testpass123')
        
        qna = QnA.objects.create(
            user=self.user,
            product=self.product,
            title='기존 Q&A',
            content='기존 내용'
        )
        
        response = self.client.post(reverse('qna:qna_edit', args=[qna.id]), {
            'title': '수정된 Q&A',
            'content': '수정된 내용',
            'is_public': True
        })
        
        self.assertEqual(response.status_code, 302)
        qna.refresh_from_db()
        self.assertEqual(qna.title, '수정된 Q&A')

    def test_qna_delete_view(self):
        """Q&A 삭제 테스트"""
        self.client.login(email='test@example.com', password='testpass123')
        
        qna = QnA.objects.create(
            user=self.user,
            product=self.product,
            title='삭제할 Q&A',
            content='삭제할 내용'
        )
        
        response = self.client.post(reverse('qna:qna_delete', args=[qna.id]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(QnA.objects.filter(id=qna.id).exists())

    def test_qna_access_control(self):
        """Q&A 접근 권한 테스트"""
        other_user = User.objects.create_user(
            email='other@example.com',
            password='testpass123'
        )
        
        qna = QnA.objects.create(
            user=other_user,
            product=self.product,
            title='다른 사용자 Q&A',
            content='다른 사용자 내용'
        )
        
        self.client.login(email='test@example.com', password='testpass123')
        
        # 다른 사용자의 Q&A 수정 시도
        response = self.client.get(reverse('qna:qna_edit', args=[qna.id]))
        self.assertEqual(response.status_code, 403)
        
        # 다른 사용자의 Q&A 삭제 시도
        response = self.client.post(reverse('qna:qna_delete', args=[qna.id]))
        self.assertEqual(response.status_code, 403)

    def test_qna_public_private_filter(self):
        """Q&A 공개/비공개 필터링 테스트"""
        public_qna = QnA.objects.create(
            user=self.user,
            product=self.product,
            title='공개 Q&A',
            content='공개 내용',
            is_public=True
        )
        
        private_qna = QnA.objects.create(
            user=self.user,
            product=self.product,
            title='비공개 Q&A',
            content='비공개 내용',
            is_public=False
        )
        
        # 비로그인 사용자는 공개 Q&A만 볼 수 있어야 함
        response = self.client.get(reverse('qna:qna_index', args=[self.product.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '공개 Q&A')
        self.assertNotContains(response, '비공개 Q&A')
        
        # 로그인한 사용자는 자신의 비공개 Q&A도 볼 수 있어야 함
        self.client.login(email='test@example.com', password='testpass123')
        response = self.client.get(reverse('qna:qna_index', args=[self.product.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '공개 Q&A')
        self.assertContains(response, '비공개 Q&A')