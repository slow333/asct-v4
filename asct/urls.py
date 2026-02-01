from django.urls import path
from . import views_basic

app_name = 'asct'

urlpatterns = [
    path('', views_basic.index, name='index'),
    
    path('command/list/', views_basic.cmd_list, name='cmd_list'),
    path('command/add/', views_basic.cmd_add, name='cmd_add'),
    path('command/detail/<int:pk>/', views_basic.cmd_detail, name='cmd_detail'),
    path('command/update/<int:pk>/', views_basic.cmd_update, name='cmd_update'),
    path('command/delete/<int:pk>/', views_basic.cmd_delete, name='cmd_delete'),
    
    path('command/select/', views_basic.cmd_select, name='cmd_select'),
    path('command/history/', views_basic.cmd_history_list, name='cmd_history_list'),
    path('command/history/delete/<int:pk>', views_basic.cmd_history_delete, name='cmd_history_delete'),
    
    path('sshinfo/list/', views_basic.sshinfo_list, name='sshinfo_list'),
    path('sshinfo/add/', views_basic.sshinfo_add, name='sshinfo_add'),
    path('sshinfo/detail/<int:pk>/', views_basic.sshinfo_detail, name='sshinfo_detail'),
    path('sshinfo/update/<int:pk>/', views_basic.sshinfo_update, name='sshinfo_update'),
    path('sshinfo/delete/<int:pk>/', views_basic.sshinfo_delete, name='sshinfo_delete'),
    
    path('run/<int:ssh_id>/<int:cmd_id>/', views_basic.run_cmd, name='run_cmd'),
    
    path('svinfo/list/', views_basic.serverinfo_list, name='serverinfo_list'),
    path('svinfo/export/', views_basic.serverinfo_export, name='serverinfo_export'),
    path('svinfo/update/<int:pk>/', views_basic.serverinfo_update, name='serverinfo_update'),
    path('svinfo/delete/<int:pk>/', views_basic.serverinfo_delete, name='serverinfo_delete'),
    path('svinfo/select/', views_basic.serverinfo_select, name='serverinfo_select'),
    path('svinfo/run/<int:ssh_id>/', views_basic.serverinfo_run, name='serverinfo_run'),
    
    # path('create/', views.blog_create, name='post-create'),
    # path('<int:pk>/update', views.blog_update, name='post-update'),
    # path('<int:pk>/delete', views.blog_delete, name='post-delete'),
    # path('<int:pk>/detail', views.blog_detail, name='post-detail'),
    # path('<str:username>/user-posts', views.blog_user_posts, name='user-posts'),
]