from django import forms
from .models import User
from . import models
from django.contrib.auth.forms import UserChangeForm

class LoginForm(forms.Form):
    """Login Form Definition"""
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'class': 'form-control',  # CSS 클래스 추가
    }),
        label="이메일(아이디)")
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',  # CSS 클래스 추가
    }),
        label="비밀번호")
    def clean(self):
        email = self.cleaned_data.get("email") # 👈 유효성 검사를 진행한 email field에 값을 추출합니다.
        password = self.cleaned_data.get("password") # 👈 유효성 검사를 진행한 password field에 값을 추출합니다.
        try:
            user = models.User.objects.get(email=email) # 👈 emil을 기준으로 해당 Object를 가져와요!
            if user.check_password(password):  # 👈 비밀번호가 서로 일치하다면 True, 아니면 False 반환
                return self.cleaned_data
            else:
                self.add_error("password", forms.ValidationError("Password is wrong"))
        except models.User.DoesNotExist:
            self.add_error("email", forms.ValidationError("User does not exist"))

class SignUpForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
    }), label="비밀번호")
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
    }), label="비밀번호 확인")

    class Meta:
        model = models.User
        fields = ['name', 'email', 'tel', 'birthday', 'postcode', 'address', 'detail_address', 'extra_address']
        labels = {
            'name': '이름',
            'email': '이메일(아이디)',
            'tel': '연락처',
            'birthday': '생년월일',
            'postcode': '우편번호',
            'address': '주소',
            'detail_address': '상세주소',
            'extra_address': '참고항목',
        }

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if models.User.objects.filter(email=email).exists():
            raise forms.ValidationError("이미 사용중인 이메일입니다.")
        return email

    def clean_password1(self):
        password = self.cleaned_data.get("password")
        password1 = self.cleaned_data.get("password1")
        if password and password1 and password != password1:
            raise forms.ValidationError("비밀번호가 일치하지 않습니다.")
        else:
            return password

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data.get("password"))
        if commit:
            user.save()
        return user

class CustomUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = User()
        fields = ('email', 'name',)

from django import forms
from .models import User

class SignupCompleteForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['name', 'tel', 'birthday']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': '이름 입력', 'maxlength': '10'}),
            'tel': forms.TextInput(attrs={'placeholder': '전화번호 입력 ("-" 제외)', 'maxlength': '11'}),
            'birthday': forms.DateInput(attrs={'type': 'date', 'placeholder': '생일 입력 (YYYY-MM-DD)'}),
        }
        labels = {
            'name': '이름',
            'tel': '전화번호',
            'birthday': '생일',
        }

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['name', 'email', 'tel', 'postcode', 'address', 'detail_address', 'extra_address', 'birthday']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'tel': forms.TextInput(attrs={'class': 'form-control'}),
            'postcode': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.TextInput(attrs={'class': 'form-control'}),
            'detail_address': forms.TextInput(attrs={'class': 'form-control'}),
            'extra_address': forms.TextInput(attrs={'class': 'form-control'}),
            'birthday': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }
        labels = {
            'name': '이름',
            'email': '이메일',
            'tel': '전화번호',
            'postcode': '우편번호',
            'address': '주소',
            'detail_address': '상세주소',
            'extra_address': '참고항목',
            'birthday': '생일',
        }
