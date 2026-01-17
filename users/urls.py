from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'users'

urlpatterns = [
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('register/', views.UserRegisterView.as_view(), name='register'),
    path('edit-profile/', views.UserEditView.as_view(), name='edit-profile'),
    path('password/', auth_views.PasswordChangeView.as_view(template_name='users/password_change.html'), name='password-change'),
]