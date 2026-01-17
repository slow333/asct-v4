from django.urls import path
from . import views

# apps/asct/
app_name = 'asct'

urlpatterns = [
    path('', views.index, name='index'),
    # path('create/', views.blog_create, name='post-create'),
    # path('<int:pk>/update', views.blog_update, name='post-update'),
    # path('<int:pk>/delete', views.blog_delete, name='post-delete'),
    # path('<int:pk>/detail', views.blog_detail, name='post-detail'),
    # path('<str:username>/user-posts', views.blog_user_posts, name='user-posts'),
]