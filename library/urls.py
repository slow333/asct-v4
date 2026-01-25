from django.urls import path
from . import views

# /app/library/
app_name = 'library'

urlpatterns = [
    path('', views.index, name='index'),
    path('books/', views.book_list, name='books'),
    path('book/create', views.book_create, name='book-create'), # type: ignore
    path('authors/', views.author_list, name='authors'),
    path('book/<int:pk>', views.book_detail, name='book-detail'),
    path('book/<int:pk>/update', views.book_update, name='book-update'), # type: ignore
    path('book/<int:pk>/delete', views.book_delete, name='book-delete'), # type: ignore
    path('author/create', views.author_create, name='author-create'), # type: ignore
    path('author/<int:pk>', views.author_detail, name='author-detail'),
    path('author/<int:pk>/update', views.author_update, name='author-update'), # type: ignore
    path('author/<int:pk>/delete', views.author_delete, name='author-delete'), # type: ignore
    path('bookinstances/', views.bookinstances, name='bookinstances'),
    path('bookinstance/create/', views.bookinstance_create, name='bookinstance-create'), # type: ignore
    path('bookinstance/create/<int:pk>/', views.bookinstance_create, name='bookinstance-create'), # type: ignore
    path('bookinstance/<uuid:pk>', views.bookinstance_detail, name='bookinstance-detail'),
    path('bookinstance/<uuid:pk>/update/', views.bookinstance_update, name='bookinstance-update'), # type: ignore
    path('bookinstance/<uuid:pk>/delete/', views.bookinstance_delete, name='bookinstance-delete'), # type: ignore
    path('bookinstance_available/', views.bookinstance_available, name='bookinstance-available'),
]