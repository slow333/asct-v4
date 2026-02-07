from django.contrib import admin
from django import forms
from django.utils.html import format_html
from django.conf import settings
from django.contrib import messages
from .models_basic import Command, SSHInfo, CommandHistory, ServerRole,ServerInfo
from .forms_basic import ServerInfoForm

@admin.register(Command)
class CommandAdmin(admin.ModelAdmin):
    list_display = ('name', 'script', 'description', 'category')
    list_editable =('category',)

@admin.register(SSHInfo)
class SSHInfoAdmin(admin.ModelAdmin):
    list_display = ('name','login_id', 'ip', 'port', 'password', 'display_operators')
    search_fields = ('ip',)
    autocomplete_fields = ['operators']
    list_filter =('operators',)

    def display_operators(self, obj):
        return ", ".join([operator.username for operator in obj.operators.all()])
    display_operators.short_description = 'Operators'

@admin.register(CommandHistory)
class CommandHistoryAdmin(admin.ModelAdmin):
    list_display = ('command', 'ssh_info', 'executed_by', 'executed_at')
    list_filter = ('executed_at', 'ssh_info', 'command')
    readonly_fields = ('stdout', 'stderr', 'executed_at')

@admin.register(ServerRole)
class ServerRoleAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name', )

@admin.action(description='Refresh selected Server Info (Async)')
def refresh_server_info(modeladmin, request, queryset):
    from .tasks import refresh_server_info_task
    count = queryset.count()
    for server_info in queryset:
        refresh_server_info_task.delay(server_info.id)
    
    modeladmin.message_user(request, f"{count} servers have been queued for background update.", messages.SUCCESS)

@admin.register(ServerInfo)
class ServerInfoAdmin(admin.ModelAdmin):
    form = ServerInfoForm
    list_display = ('hostname', 'ip1', 'cpu_usage_colored', 'memory_usage_colored', 'disk_usage_colored', 'uptime', 'data_time', 'is_virtual', 'is_confirmed')
    search_fields = ('hostname', 'ip1', 'roles__name')
    list_filter = ('is_virtual', 'is_master', 'is_confirmed')
    date_hierarchy = 'data_time'
    ordering = ('hostname','-data_time',)
    actions = [refresh_server_info]

    def display_roles(self, obj):
        return obj.roles.name if obj.roles else ""
    display_roles.short_description = 'Server Roles'

    def cpu_usage_colored(self, obj):
        if obj.cpu_usage is None:
            return '-'
        color = 'red' if obj.cpu_usage >= 80 else 'black'
        return format_html('<span style="color: {}; font-weight: bold;">{}%</span>', color, obj.cpu_usage)
    cpu_usage_colored.short_description = 'CPU(%)'
    cpu_usage_colored.admin_order_field = 'cpu_usage'

    def memory_usage_colored(self, obj):
        if obj.memory_usage is None:
            return '-'
        color = 'red' if obj.memory_usage >= 80 else 'black'
        return format_html('<span style="color: {}; font-weight: bold;">{}%</span>', color, obj.memory_usage)
    memory_usage_colored.short_description = 'Mem(%)'
    memory_usage_colored.admin_order_field = 'memory_usage'

    def disk_usage_colored(self, obj):
        if obj.disk_usage is None:
            return '-'
        color = 'red' if obj.disk_usage >= 80 else 'black'
        return format_html('<span style="color: {}; font-weight: bold;">{}%</span>', color, obj.disk_usage)
    disk_usage_colored.short_description = 'Disk(%)'
    disk_usage_colored.admin_order_field = 'disk_usage'