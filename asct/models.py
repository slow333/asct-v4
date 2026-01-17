from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Operator(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    
    alias_name = models.CharField(max_length=50, blank=True, null=True)
    
    mobile_number = models.CharField(max_length=20, blank=True, null=True)
    office_number = models.CharField(max_length=20, blank=True, null=True)
    
    email = models.EmailField(blank=True, null=True)
    
    compay_name = models.CharField(max_length=100, blank=True, null=True)
    company_address = models.CharField(max_length=255, blank=True, null=True)
    
    department = models.CharField(max_length=100, blank=True, null=True)
    
    team = models.CharField(max_length=100, blank=True, null=True)
    position = models.CharField(max_length=100, blank=True, null=True)
    role = models.CharField(max_length=255, blank=True, null=True)
    
    is_active = models.BooleanField(default=True, null=False)
    is_manager = models.BooleanField(default=False, null=False)
    is_online = models.BooleanField(default=True, null=False)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def save(self, *args, **kwargs):
        if not self.alias_name:
            self.alias_name = self.user.username
        super().save(*args, **kwargs)
    
    def __str__(self) -> str:
        return self.alias_name or self.user.username

class SSHInfo(models.Model):
    operator = models.ForeignKey(Operator, on_delete=models.PROTECT, null=False)
    
    login_id = models.CharField(max_length=20, null=False)
    ip = models.GenericIPAddressField(null=False)
    port = models.IntegerField(default=22, null=False)
    password = models.CharField(max_length=255, blank=True, null=True)
    
    start_date = models.DateField(default=timezone.now)
    end_date = models.DateField(blank=True, null=True)
    
    is_active = models.BooleanField(default=True, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self) -> str:
        return f'SSH Info: {self.login_id}@{self.ip}:{self.port}'

class ServerRole(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

class ServerInfo(models.Model):
    sshinfo = models.ManyToManyField(SSHInfo)
    
    hostname = models.CharField(max_length=100, null=False)
    server_roles = models.ManyToManyField(ServerRole, blank=True)
    role_version = models.CharField(max_length=255, null=False) # apache 2.4, mysql 8.2
    
    ip_real = models.GenericIPAddressField(null=False)
    
    os_version = models.CharField(max_length=100, null=False) # e.g.,RHEL 7, etc.
    kernel_version = models.CharField(max_length=255, null=False)
    cpu_cores = models.PositiveSmallIntegerField(null=True, blank=True)
    total_memory = models.PositiveSmallIntegerField(null=False) # GB 단위
    total_disk = models.PositiveSmallIntegerField(null=False) # GB 단위
    uptime = models.PositiveSmallIntegerField(null=False) # in days
    
    is_virtual = models.BooleanField(default=True, null=False) # 가상서버여부
    is_master = models.BooleanField(default=True, null=False) # 마스터서버여부
    
    created_at = models.DateTimeField(auto_now_add=True)
    comment = models.TextField(null=True)
    is_confirmed = models.BooleanField(default=False, null=False)
    
    def __str__(self) -> str:
        return f'{self.hostname} ({self.ip_real})'
    
    class Meta:
        ordering = ['hostname','-created_at']
        unique_together = ('hostname','ip_real', 'created_at')

class CPUUsage(models.Model):
    serverinfo = models.ForeignKey(ServerInfo, on_delete=models.PROTECT)
    
    usage_percent = models.DecimalField(max_digits=8, decimal_places=2, null=False)
    datetime = models.DateTimeField(null=False)
    
    created_at = models.DateTimeField(auto_now_add=True)
    comment = models.TextField(null=True, blank=True)
    is_confirmed = models.BooleanField(default=False, null=False)
    
    def cpu_core_count(self):
        return self.serverinfo.cpu_cores
    
    def __str__(self) -> str:
        return f'CPU Usage for {self.serverinfo.hostname}'
    
    class Meta:
        ordering = ['serverinfo__hostname','-datetime']
        unique_together = ('serverinfo','datetime')

class MemoryUsage(models.Model):
    serverinfo = models.ForeignKey(ServerInfo, on_delete=models.PROTECT)
    
    def total_memory(self):
        return self.serverinfo.total_memory
    usage_percent = models.DecimalField(max_digits=4, decimal_places=2, null=False)
    datetime = models.DateTimeField(null=False)
    
    created_at = models.DateTimeField(auto_now_add=True)
    comment = models.TextField(null=True, blank=True)
    is_confirmed = models.BooleanField(default=False, null=False)
    
    def __str__(self) -> str:
        return f'Memory Usage for {self.serverinfo.hostname}'
    
    class Meta:
        ordering = ['serverinfo__hostname','-datetime']
        unique_together = ('serverinfo', 'datetime')

class DiskUsage(models.Model):
    serverinfo = models.ForeignKey(ServerInfo, on_delete=models.PROTECT)
    
    storage_local_total = models.IntegerField(null=False) 
    storage_local_usage_percent = models.DecimalField(max_digits=4, decimal_places=2, null=False)
    datetime = models.DateTimeField(null=False)
    
    created_at = models.DateTimeField(auto_now_add=True)
    comment = models.TextField(null=True, blank=True)
    is_confirmed = models.BooleanField(default=False, null=False)
    
    def __str__(self) -> str:
        return f'Disk Usage for {self.serverinfo.hostname}'
    
    class Meta:
        ordering = ['serverinfo__hostname','-datetime']
        unique_together = ('serverinfo', 'datetime')

class NetworkUsage(models.Model):
    serverinfo = models.ForeignKey(ServerInfo, on_delete=models.PROTECT)
    
    network_type = [
        ('100M','100M'),('1G','1G'), ('10G','10G'), ('40G','40G'), ('100G','100G'), 
        ('8G','8G FC'), ('16G','16G FC'), ('32G','32G FC'), ('64G','64G FC')]
    network_service = models.CharField(max_length=10, choices=network_type, default='1G', null=False)
    network_service_inbound_bytes = models.DecimalField(max_digits=20, decimal_places=2, null=False)
    network_service_outbound_bytes = models.DecimalField(max_digits=20, decimal_places=2, null=False)
    datetime = models.DateTimeField(null=False)
    
    created_at = models.DateTimeField(auto_now_add=True)
    comment = models.TextField(null=True, blank=True)
    is_confirmed = models.BooleanField(default=False)
    
    def __str__(self) -> str:
        return f'Network Usage for {self.serverinfo.hostname}'
    
    class Meta:
        ordering = ['serverinfo__hostname','-datetime']
        unique_together = ('serverinfo', 'datetime')

class SysctlParameter(models.Model):
    name = models.CharField(max_length=255, unique=True, null=False)
    description = models.TextField(null=True, blank=True)

    def __str__(self) -> str:
        return self.name

    class Meta:
        ordering = ['name']

class SysctlSetting(models.Model):
    serverinfo = models.ForeignKey(ServerInfo, on_delete=models.PROTECT)
    
    parameter = models.ForeignKey(SysctlParameter, on_delete=models.PROTECT)
    value = models.CharField(max_length=255, null=False)
    
    created_at =models.DateTimeField(auto_now_add=True)
    comment = models.TextField(null=True, blank=True)
    is_confirmed = models.BooleanField(default=False, null=False)
    
    def __str__(self) -> str:
        return f'Sysctl {self.parameter.name} for {self.serverinfo.hostname}'
    
    class Meta:
        ordering = ['serverinfo','-created_at']
        unique_together = ('serverinfo','created_at',)

class SystemLog(models.Model):
    serverinfo = models.ForeignKey(ServerInfo, on_delete=models.PROTECT)
    
    log_level_choices = [
        ('DEBUG','DEBUG'),('INFO','INFO'), ('WARNING','WARNING'), ('ERROR','ERROR'), ('CRITICAL','CRITICAL')]
    
    log_level = models.CharField(max_length=10, choices=log_level_choices, null=False, default='ERROR')
    log_message = models.TextField(null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    comment = models.TextField(null=True, blank=True)
    is_confirmed = models.BooleanField(default=False, null=False)
    
    def save(self, *args, **kwargs):
        # 개발시는 전체 저장
        if any(level in self.log_message.lower() for level in ['error', 'info', 'warning', 'critical', 'debug']): # type: ignore
            super().save(*args, **kwargs)
        # 'error' 또는 'info'가 없으면 아무 작업도 하지 않아 저장을 건너뜁니다.

    def __str__(self) -> str:
        return f'Log from {self.serverinfo.hostname} at {self.created_at}'
    
    class Meta:
        ordering = ['serverinfo','-created_at']
        unique_together = ('serverinfo', 'created_at')

class Command(models.Model):
    name = models.CharField(max_length=255, unique=True, null=False)
    script = models.TextField(null=False)
    description = models.TextField(null=True, blank=True)

    def __str__(self) -> str:
        return self.name

    class Meta:
        ordering = ['name']

