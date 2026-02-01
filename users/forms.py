from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import Profile
from django.utils.safestring import mark_safe

class UserRegisterForm(UserCreationForm):
    # 추가 필드 정의 했지만 templet에서 crispy-forms을 적용해서 자동으로 처리함
    username = forms.CharField(
        label='사용자명', widget=forms.TextInput(
        attrs={'class': 'form-control'}), 
        help_text='이름은 3자 이상을 넣으세요')
    email = forms.EmailField(
        label='이메일', 
        widget=forms.EmailInput(attrs={'class': 'form-control'}))
    password1 = forms.CharField(
        label='암호', 
        widget=forms.PasswordInput(
            attrs={'class': 'form-control', 'placeholder': '암호 확인', 'type': 'password',}),
        help_text = mark_safe('<ul class="list-unstyled text-muted small" style="margin-bottom: 0;">' \
            '<li>암호는 8자 이상입니다.</li>'\
            '<li>암호는 username하고 유사하면 안되요.</li>'\
            '<li>암호는 숫자만으로 구성되면 안되요.</li>'\
            '<li>암호는 일반적으로 사용되는 것은 안되요.</li>'\
        '</ul>'))
    password2 = forms.CharField(
        label='암호', 
        widget=forms.PasswordInput(
            attrs={'class': 'form-control', 'placeholder': '암호 확인', 'type': 'password'}),
        help_text = '위에 암호와 같은 암호를 적으세요.')

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    error_messages = {
        'password_mismatch': "암호는 2개가 같아야 합니다.",
    }

class UserUpdateForm(forms.ModelForm):
    username = forms.CharField(
        label='사용자명(이름은 3자 이상을 넣으세요)', widget=forms.TextInput(
        attrs={'class': 'form-control'}), 
    )
    email = forms.EmailField(required=False, widget=forms.EmailInput(attrs={'class': 'form-control mb-3'}))
    first_name = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control mb-3'}), label='이름',)
    last_name = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control mb-3'}), label='성',)

    class Meta:
        model = User
        fields = ['username', 'email', 'last_name', 'first_name']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control mb-3'}),
        }
        error_messages = {
            'username': {'required': ''},
        }

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image', 'role']
        widgets = {
            'image': forms.FileInput(attrs={'class': 'form-control mb-3'}),
            'role': forms.Select(attrs={'class': 'form-select mb-3'}),
        }
        error_messages = {
            'image': {'required': ''},
        }

class LoginForm(forms.Form):
    username = forms.CharField(max_length=65, widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(max_length=65, widget=forms.PasswordInput(attrs={'class': 'form-control'}, render_value=True))