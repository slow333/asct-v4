from django.contrib import admin
from .models import SSHInfo, ServerInfo, CPUUsage, MemoryUsage, DiskUsage, NetworkUsage, SysctlParameter,SysctlSetting, SystemLog, ServerRole, Operator

@admin.register(Operator)
class OperatorAdmin(admin.ModelAdmin):
    list_display = ('user', 'alias_name', 'mobile_number', 'office_number', 'email', 'compay_name', 'department', 'team', 'position', 'role', 'is_active', 'is_manager', 'is_online', 'created_at', 'updated_at')
    list_filter = ('is_active', 'is_manager', 'is_online')

class ServerInfoInline(admin.TabularInline):
    model = ServerInfo.sshinfo.through # many to many 일 때 
    extra = 0

@admin.register(SSHInfo)
class SSHInfoAdmin(admin.ModelAdmin):
    list_display = ('login_id', 'ip', 'port', 'password', 'start_date', 'end_date', 'is_active', 'created_at')
    list_filter = ('is_active',)
    search_fields = ('ip',)
    inlines = [ServerInfoInline]

@admin.register(ServerRole)
class ServerRoleAdmin(admin.ModelAdmin):
    list_display = ('name', )
    search_fields = ('name', )

@admin.register(ServerInfo)
class ServerInfoAdmin(admin.ModelAdmin):
    list_display = ('hostname', 'get_sshinfo', 'get_server_roles', 'os_version','kernel_version','cpu_cores', 'total_memory', 'total_disk', 'uptime', 'is_virtual', 'is_master', 'created_at', 'comment','is_confirmed')
    search_fields = ('hostname', 'ip_real', 'server_roles__name')
    list_filter = ('is_virtual', 'is_master', 'is_confirmed')
    date_hierarchy = 'created_at'
    ordering = ('hostname','-created_at',)

    def get_sshinfo(self, obj):
        return ", ".join([f"{ssh.login_id}@{ssh.ip}" for ssh in obj.sshinfo.all()])
    get_sshinfo.short_description = 'SSH Info'

    def get_server_roles(self, obj):
        return ", ".join([role.name for role in obj.server_roles.all()])
    get_server_roles.short_description = 'Server Roles'

@admin.register(CPUUsage)
class CPUUsageAdmin(admin.ModelAdmin):
    list_display = ('serverinfo__hostname', 'usage_percent', 'datetime')
    search_fields = ('serverinfo__hostname','usage_percent')
    ordering = ('serverinfo__hostname','-datetime')

@admin.register(MemoryUsage)
class MemoryUsageAdmin(admin.ModelAdmin):
    list_display = ('serverinfo__hostname', 'usage_percent', 'datetime')
    search_fields = ('serverinfo__hostname','usage_percent')
    ordering = ('serverinfo__hostname','-datetime')

@admin.register(DiskUsage)
class DiskUsageAdmin(admin.ModelAdmin):
    list_display = ('serverinfo__hostname', 'storage_local_usage_percent', 'datetime')
    search_fields = ('serverinfo__hostname',)
    ordering = ('serverinfo__hostname','-datetime')

@admin.register(NetworkUsage)
class NetworkUsageAdmin(admin.ModelAdmin):
    list_display = ('serverinfo__hostname', 'network_service','network_service_inbound_bytes', 'network_service_outbound_bytes', 'datetime')
    search_fields = ('serverinfo__hostname',)
    ordering = ('serverinfo__hostname','-datetime')

@admin.register(SysctlParameter)
class SysctlParameterAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')

@admin.register(SysctlSetting)
class SysctlSettingAdmin(admin.ModelAdmin):
    list_display = ('serverinfo__hostname', 'parameter', 'value', 'created_at')
    search_fields = ('serverinfo__hostname', 'parameter')
    ordering = ('serverinfo__hostname','parameter','-created_at')

@admin.register(SystemLog)
class SystemLogAdmin(admin.ModelAdmin):
    list_display = ('serverinfo__hostname', 'log_level', 'log_message', 'created_at')
    search_fields = ('serverinfo__hostname', 'log_message')
    ordering = ('serverinfo__hostname','-created_at')