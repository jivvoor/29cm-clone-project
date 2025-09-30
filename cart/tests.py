from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.contrib.sessions.models import Session
from shop.models import Product, Category, SubCategory, SizeCategory, ColorCategory
from .models import Cart, CartItem

User = get_user_model()


class CartModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='test@example.com',
            password='testpass123'
        )
        self.category = Category.objects.create(name='테스트 카테고리', slug='test-category')
        self.subcategory = SubCategory.objects.create(
            name='테스트 서브카테고리', 
            slug='test-subcategory',
            category=self.category
        )
        self.size = SizeCategory.objects.create(name='M')
        self.color = ColorCategory.objects.create(name='빨강')
        self.product = Product.objects.create(
            name='테스트 상품',
            price=10000,
            description='테스트 상품입니다',
            category=self.category,
            subcategory=self.subcategory
        )

    def test_cart_creation_for_authenticated_user(self):
        """로그인한 사용자의 장바구니 생성 테스트"""
        cart = Cart.objects.create(user=self.user)
        self.assertEqual(cart.user, self.user)
        self.assertIsNone(cart.cart_id)

    def test_cart_creation_for_anonymous_user(self):
        """비로그인 사용자의 장바구니 생성 테스트"""
        cart = Cart.objects.create(cart_id='test-session-id')
        self.assertEqual(cart.cart_id, 'test-session-id')
        self.assertIsNone(cart.user)

    def test_cart_item_creation(self):
        """장바구니 아이템 생성 테스트"""
        cart = Cart.objects.create(user=self.user)
        cart_item = CartItem.objects.create(
            cart=cart,
            product=self.product,
            size=self.size,
            color=self.color,
            quantity=2
        )
        
        self.assertEqual(cart_item.cart, cart)
        self.assertEqual(cart_item.product, self.product)
        self.assertEqual(cart_item.quantity, 2)
        self.assertEqual(cart_item.sub_total(), 20000)

    def test_cart_item_unique_constraint(self):
        """장바구니 아이템 유니크 제약조건 테스트"""
        cart = Cart.objects.create(user=self.user)
        
        # 첫 번째 아이템 생성
        CartItem.objects.create(
            cart=cart,
            product=self.product,
            size=self.size,
            color=self.color,
            quantity=1
        )
        
        # 같은 조건으로 두 번째 아이템 생성 시도 (실패해야 함)
        with self.assertRaises(Exception):  # IntegrityError 또는 ValidationError
            CartItem.objects.create(
                cart=cart,
                product=self.product,
                size=self.size,
                color=self.color,
                quantity=1
            )


class CartViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            email='test@example.com',
            password='testpass123'
        )
        self.category = Category.objects.create(name='테스트 카테고리', slug='test-category')
        self.subcategory = SubCategory.objects.create(
            name='테스트 서브카테고리', 
            slug='test-subcategory',
            category=self.category
        )
        self.size = SizeCategory.objects.create(name='M')
        self.color = ColorCategory.objects.create(name='빨강')
        self.product = Product.objects.create(
            name='테스트 상품',
            price=10000,
            description='테스트 상품입니다',
            category=self.category,
            subcategory=self.subcategory
        )

    def test_add_cart_authenticated_user(self):
        """로그인한 사용자의 장바구니 추가 테스트"""
        self.client.login(email='test@example.com', password='testpass123')
        
        response = self.client.post(reverse('cart:add_cart', args=[self.product.id]), {
            'quantity': 1,
            'sizecategory': self.size.id,
            'colorcategory': self.color.id
        })
        
        self.assertEqual(response.status_code, 302)
        self.assertTrue(CartItem.objects.filter(
            cart__user=self.user,
            product=self.product
        ).exists())

    def test_add_cart_anonymous_user(self):
        """비로그인 사용자의 장바구니 추가 테스트"""
        response = self.client.post(reverse('cart:add_cart', args=[self.product.id]), {
            'quantity': 1,
            'sizecategory': self.size.id,
            'colorcategory': self.color.id
        })
        
        self.assertEqual(response.status_code, 302)
        # 세션 기반 장바구니가 생성되었는지 확인
        self.assertTrue(Cart.objects.filter(cart_id__isnull=False).exists())

    def test_cart_detail_authenticated_user(self):
        """로그인한 사용자의 장바구니 상세보기 테스트"""
        self.client.login(email='test@example.com', password='testpass123')
        
        cart = Cart.objects.create(user=self.user)
        CartItem.objects.create(
            cart=cart,
            product=self.product,
            size=self.size,
            color=self.color,
            quantity=2
        )
        
        response = self.client.get(reverse('cart:cart_detail'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.product.name)
        self.assertEqual(response.context['total'], 20000)
        self.assertEqual(response.context['counter'], 2)

    def test_delete_item_authenticated_user(self):
        """로그인한 사용자의 아이템 삭제 테스트"""
        self.client.login(email='test@example.com', password='testpass123')
        
        cart = Cart.objects.create(user=self.user)
        cart_item = CartItem.objects.create(
            cart=cart,
            product=self.product,
            size=self.size,
            color=self.color,
            quantity=1
        )
        
        response = self.client.post(reverse('cart:delete_item'), {
            'cart_item_id': cart_item.id
        })
        
        self.assertEqual(response.status_code, 200)
        self.assertFalse(CartItem.objects.filter(id=cart_item.id).exists())

    def test_delete_item_access_denied(self):
        """다른 사용자의 아이템 삭제 시도 테스트"""
        other_user = User.objects.create_user(
            email='other@example.com',
            password='testpass123'
        )
        self.client.login(email='test@example.com', password='testpass123')
        
        other_cart = Cart.objects.create(user=other_user)
        other_cart_item = CartItem.objects.create(
            cart=other_cart,
            product=self.product,
            size=self.size,
            color=self.color,
            quantity=1
        )
        
        response = self.client.post(reverse('cart:delete_item'), {
            'cart_item_id': other_cart_item.id
        })
        
        self.assertEqual(response.status_code, 403)

    def test_update_quantity(self):
        """장바구니 수량 업데이트 테스트"""
        self.client.login(email='test@example.com', password='testpass123')
        
        cart = Cart.objects.create(user=self.user)
        cart_item = CartItem.objects.create(
            cart=cart,
            product=self.product,
            size=self.size,
            color=self.color,
            quantity=1
        )
        
        response = self.client.post(reverse('cart:update_quantity'), {
            'cart_item_id': cart_item.id,
            'quantity': 5
        })
        
        self.assertEqual(response.status_code, 200)
        cart_item.refresh_from_db()
        self.assertEqual(cart_item.quantity, 5)

    def test_delete_selected_items(self):
        """선택된 아이템들 삭제 테스트"""
        self.client.login(email='test@example.com', password='testpass123')
        
        cart = Cart.objects.create(user=self.user)
        cart_item1 = CartItem.objects.create(
            cart=cart,
            product=self.product,
            size=self.size,
            color=self.color,
            quantity=1
        )
        cart_item2 = CartItem.objects.create(
            cart=cart,
            product=self.product,
            size=self.size,
            color=self.color,
            quantity=1
        )
        
        response = self.client.post(reverse('cart:delete_selected_items'), {
            'selected_items': [cart_item1.id, cart_item2.id]
        })
        
        self.assertEqual(response.status_code, 302)
        self.assertFalse(CartItem.objects.filter(id__in=[cart_item1.id, cart_item2.id]).exists())