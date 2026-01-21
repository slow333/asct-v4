from django.urls import path # type: ignore
from . import views

# apps/blog/
app_name = 'blog'

urlpatterns = [
    path('', views.post_list, name='index'),
    path('<int:pk>', views.post_list, name='index'),
    path('add/', views.add_post, name='add'),
    path('<int:pk>/update', views.update_post, name='update'),
    path('<int:pk>/delete', views.delete_post, name='delete'),
    path('<int:pk>/detail', views.post_detail, name='detail'),
    path('<str:username>/user-posts', views.user_post_list, name='user-posts'),
    path('<int:pk>/like', views.like_post, name='like-post'), # type: ignore
    path('<int:pk>/add-comment', views.add_comment, name='add-comment'),
    path('<int:pk>/delete-comment', views.delete_comment, name='delete-comment'),
    path('<int:pk>/edit-comment', views.edit_comment, name='edit-comment'),
]
