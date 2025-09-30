from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.contrib.sessions.models import Session

User = get_user_model()


class UserModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='test@example.com',
            password='testpass123',
            first_name='테스트',
            last_name='사용자'
        )

    def test_user_creation(self):
        """사용자 생성 테스트"""
        self.assertEqual(self.user.email, 'test@example.com')
        self.assertTrue(self.user.check_password('testpass123'))
        self.assertEqual(self.user.first_name, '테스트')
        self.assertEqual(self.user.last_name, '사용자')

    def test_user_str_method(self):
        """사용자 __str__ 메서드 테스트"""
        self.assertEqual(str(self.user), 'test@example.com')

    def test_user_full_name(self):
        """사용자 전체 이름 테스트"""
        self.assertEqual(self.user.get_full_name(), '테스트 사용자')

    def test_user_short_name(self):
        """사용자 짧은 이름 테스트"""
        self.assertEqual(self.user.get_short_name(), '테스트')


class UserViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            email='test@example.com',
            password='testpass123'
        )

    def test_user_registration_view(self):
        """사용자 회원가입 뷰 테스트"""
        response = self.client.get(reverse('users:register'))
        self.assertEqual(response.status_code, 200)

    def test_user_login_view(self):
        """사용자 로그인 뷰 테스트"""
        response = self.client.get(reverse('users:login'))
        self.assertEqual(response.status_code, 200)

    def test_user_logout_view(self):
        """사용자 로그아웃 뷰 테스트"""
        self.client.login(email='test@example.com', password='testpass123')
        response = self.client.post(reverse('users:logout'))
        self.assertEqual(response.status_code, 302)

    def test_user_profile_view_authenticated(self):
        """로그인한 사용자의 프로필 뷰 테스트"""
        self.client.login(email='test@example.com', password='testpass123')
        response = self.client.get(reverse('users:profile'))
        self.assertEqual(response.status_code, 200)

    def test_user_profile_view_unauthenticated(self):
        """비로그인 사용자의 프로필 뷰 테스트"""
        response = self.client.get(reverse('users:profile'))
        self.assertEqual(response.status_code, 302)  # 리다이렉트

    def test_user_profile_update(self):
        """사용자 프로필 업데이트 테스트"""
        self.client.login(email='test@example.com', password='testpass123')
        
        response = self.client.post(reverse('users:profile_update'), {
            'first_name': '수정된',
            'last_name': '이름',
            'email': 'updated@example.com'
        })
        
        self.assertEqual(response.status_code, 302)
        self.user.refresh_from_db()
        self.assertEqual(self.user.first_name, '수정된')
        self.assertEqual(self.user.last_name, '이름')


class UserAuthenticationTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            email='test@example.com',
            password='testpass123'
        )

    def test_successful_login(self):
        """성공적인 로그인 테스트"""
        response = self.client.post(reverse('users:login'), {
            'email': 'test@example.com',
            'password': 'testpass123'
        })
        self.assertEqual(response.status_code, 302)

    def test_failed_login(self):
        """실패한 로그인 테스트"""
        response = self.client.post(reverse('users:login'), {
            'email': 'test@example.com',
            'password': 'wrongpassword'
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'error')  # 에러 메시지가 있는지 확인

    def test_logout_clears_session(self):
        """로그아웃 시 세션 클리어 테스트"""
        self.client.login(email='test@example.com', password='testpass123')
        
        # 로그인 후 세션이 있는지 확인
        self.assertTrue(self.client.session.session_key)
        
        # 로그아웃
        self.client.post(reverse('users:logout'))
        
        # 세션이 클리어되었는지 확인
        self.assertFalse(self.client.session.session_key)


class UserRegistrationTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_user_registration_success(self):
        """성공적인 회원가입 테스트"""
        response = self.client.post(reverse('users:register'), {
            'email': 'newuser@example.com',
            'password1': 'newpass123',
            'password2': 'newpass123',
            'first_name': '새로운',
            'last_name': '사용자'
        })
        
        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(email='newuser@example.com').exists())

    def test_user_registration_password_mismatch(self):
        """비밀번호 불일치 회원가입 테스트"""
        response = self.client.post(reverse('users:register'), {
            'email': 'newuser@example.com',
            'password1': 'newpass123',
            'password2': 'differentpass',
            'first_name': '새로운',
            'last_name': '사용자'
        })
        
        self.assertEqual(response.status_code, 200)
        self.assertFalse(User.objects.filter(email='newuser@example.com').exists())

    def test_user_registration_duplicate_email(self):
        """중복 이메일 회원가입 테스트"""
        User.objects.create_user(
            email='existing@example.com',
            password='testpass123'
        )
        
        response = self.client.post(reverse('users:register'), {
            'email': 'existing@example.com',
            'password1': 'newpass123',
            'password2': 'newpass123',
            'first_name': '새로운',
            'last_name': '사용자'
        })
        
        self.assertEqual(response.status_code, 200)
        # 같은 이메일로 두 명의 사용자가 생성되지 않았는지 확인
        self.assertEqual(User.objects.filter(email='existing@example.com').count(), 1)