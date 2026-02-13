from django.urls import path
from . import views_basic
from . import views_resource
from . import views_dashboard
app_name = 'asct'

urlpatterns = [
    # path('', views_basic.index, name='index'),
    path('', views_dashboard.dashboard, name='index'),
    
    path('command/list/', views_basic.cmd_list, name='cmd_list'),
    path('command/add/', views_basic.cmd_add, name='cmd_add'),
    path('command/detail/<int:pk>/', views_basic.cmd_detail, name='cmd_detail'),
    path('command/update/<int:pk>/', views_basic.cmd_update, name='cmd_update'),
    path('command/delete/<int:pk>/', views_basic.cmd_delete, name='cmd_delete'),
    
    path('command/select/', views_basic.cmd_select, name='cmd_select'),
    path('command/history/', views_basic.cmd_history_list, name='cmd_history_list'),
    path('command/history/delete/<int:pk>', views_basic.cmd_history_delete, name='cmd_history_delete'),
    path('command/run/<int:ssh_id>/<int:cmd_id>/', views_basic.cmd_run, name='cmd_run'),
    
    path('sshinfo/list/', views_basic.sshinfo_list, name='sshinfo_list'),
    path('sshinfo/add/', views_basic.sshinfo_add, name='sshinfo_add'),
    path('sshinfo/detail/<int:pk>/', views_basic.sshinfo_detail, name='sshinfo_detail'),
    path('sshinfo/update/<int:pk>/', views_basic.sshinfo_update, name='sshinfo_update'),
    path('sshinfo/delete/<int:pk>/', views_basic.sshinfo_delete, name='sshinfo_delete'),
    
    path('svinfo/list/', views_basic.serverinfo_list, name='serverinfo_list'),
    path('svinfo/export/', views_basic.serverinfo_export, name='serverinfo_export'),
    path('svinfo/update/<int:pk>/', views_basic.serverinfo_update, name='serverinfo_update'),
    path('svinfo/delete/<int:pk>/', views_basic.serverinfo_delete, name='serverinfo_delete'),
    path('svinfo/select/', views_basic.serverinfo_select, name='serverinfo_select'),
    path('svinfo/run/<int:ssh_id>/', views_basic.serverinfo_run, name='serverinfo_run'),
    
    path('cpu_usage/list/', views_resource.cpu_usage_list, name='cpu_usage_list'),
    path('cpu_usage/export/', views_resource.cpu_usage_export, name='cpu_usage_export'),
    path('cpu_usage/select/', views_resource.cpu_usage_select, name='cpu_usage_select'),
    path('cpu_usage/chart/', views_resource.cpu_usage_chart, name='cpu_usage_chart'),
    path('cpu_usage/run/<int:ssh_id>/', views_resource.cpu_usage_run, name='cpu_usage_run'),
    
    path('memory_usage/list/', views_resource.memory_usage_list, name='memory_usage_list'),
    path('memory_usage/export/', views_resource.memory_usage_export, name='memory_usage_export'),
    path('memory_usage/select/', views_resource.memory_usage_select, name='memory_usage_select'),
    path('memory_usage/chart/', views_resource.memory_usage_chart, name='memory_usage_chart'),
    path('memory_usage/run/<int:ssh_id>/', views_resource.memory_usage_run, name='memory_usage_run'),
    
    path('traffic_usage/list/', views_resource.traffic_usage_list, name='traffic_usage_list'),
    path('traffic_usage/export/', views_resource.traffic_usage_export, name='traffic_usage_export'),
    path('traffic_usage/select/', views_resource.traffic_usage_select, name='traffic_usage_select'),
    path('traffic_usage/chart/', views_resource.traffic_usage_chart, name='traffic_usage_chart'),
    path('traffic_usage/run/<int:ssh_id>/', views_resource.traffic_usage_run, name='traffic_usage_run'),
    
    path('disk_usage/list/', views_resource.disk_usage_list, name='disk_usage_list'),
    path('disk_usage/export/', views_resource.disk_usage_export, name='disk_usage_export'),
    path('disk_usage/chart/', views_resource.disk_usage_chart, name='disk_usage_chart'),
]