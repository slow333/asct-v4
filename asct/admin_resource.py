from django.contrib import admin
from .models_resource import CPUUsage

@admin.register(CPUUsage)
class CPUUsageAdmin(admin.ModelAdmin):
    list_display = ('ssh_info', 'hostname','ip','cpu_cores','usage_p', 'data_time','comment','is_confirmed')
    search_fields = ('hostname',)
    ordering = ('hostname','-data_time',)
    list_filter = ('is_confirmed','ssh_info__name')

# @admin.register(MemoryUsage)
# class MemoryUsageAdmin(admin.ModelAdmin):
#     list_display = ('serverinfo__hostname', 'usage_p', 'data_time')
#     search_fields = ('serverinfo__hostname','usage_p')
#     ordering = ('serverinfo__hostname','-data_time')
#     list_filter = ('is_confirmed',)

# @admin.register(DiskUsage)
# class DiskUsageAdmin(admin.ModelAdmin):
#     list_display = ('serverinfo__hostname', 'storage_local_total','storage_local_usage_p', 'data_time')
#     search_fields = ('serverinfo__hostname',)
#     ordering = ('serverinfo__hostname','-data_time')
#     list_filter = ('is_confirmed',)

# @admin.register(NetworkUsage)
# class NetworkUsageAdmin(admin.ModelAdmin):
#     list_display = ('serverinfo__hostname', 'network_service','in_bytes', 'out_bytes', 'data_time')
#     search_fields = ('serverinfo__hostname',)
#     ordering = ('serverinfo__hostname','-data_time')
#     list_filter = ('is_confirmed',)

# @admin.register(SysctlSetting)
# class SysctlSettingAdmin(admin.ModelAdmin):
#     list_display = ('serverinfo__hostname', 'name','description', 'value', 'data_time', 'comment')
#     search_fields = ('serverinfo__hostname', 'name')
#     ordering = ('serverinfo__hostname','name','-data_time')
#     list_filter = ('is_confirmed',)

# @admin.register(SystemLog)
# class SystemLogAdmin(admin.ModelAdmin):
#     list_display = ('serverinfo__hostname', 'log_level', 'messages', 'data_time')
#     search_fields = ('serverinfo__hostname', 'messages')
#     ordering = ('serverinfo__hostname','-data_time')
#     list_filter = ('is_confirmed',)