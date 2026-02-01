from django.db import models
from django.contrib.auth.models import User

class Command(models.Model):
    CATEGORY = (
        ('os', 'Operating System'),
        ('basic', 'Basic Shell'),
        ('app','Application'),
        ('traffic','Traffic'),
        ('sysctl','System ctl'),
        ('etc', '기타')
    )
    name = models.CharField(max_length=255, unique=True, null=False)
    script = models.TextField(null=False)
    description = models.TextField(null=True, blank=True)
    category = models.CharField(max_length=10, choices=CATEGORY, default='os')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.name

    class Meta:
        ordering = ['name']

class CommandHistory(models.Model):
    ssh_info = models.ForeignKey('SSHInfo', on_delete=models.CASCADE)
    command = models.ForeignKey(Command, on_delete=models.SET_NULL, null=True)
    executed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    
    stdout = models.TextField(blank=True)
    stderr = models.TextField(blank=True)
    
    executed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f'{self.command} on {self.ssh_info} ({self.executed_at})'

    class Meta:
        ordering = ['-executed_at']

class SSHInfo(models.Model):
    operators = models.ManyToManyField(User)

    name = models.CharField(max_length=50)
    login_id = models.CharField(max_length=50)
    ip = models.GenericIPAddressField()
    port = models.IntegerField(default=22, null=False)
    password = models.CharField(max_length=255)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self) -> str:
        return f'{self.login_id}@{self.ip}:{self.port}'

class ServerRole(models.Model):
    name = models.CharField(max_length=20, unique=True)
    description = models.CharField(max_length=100, blank=True)

    def __str__(self) -> str:
        return self.name

class ServerInfo(models.Model):
    sshinfos = models.ForeignKey(SSHInfo, on_delete=models.SET_NULL, null=True)
    roles = models.ManyToManyField(ServerRole, blank=True)
    
    hostname = models.CharField(max_length=100, null=False)
    
    ip1 = models.GenericIPAddressField(null=True, blank=True)
    ip2 = models.GenericIPAddressField(null=True, blank=True)
    
    os_version = models.CharField(max_length=100, null=False) # e.g.,RHEL 7, etc.
    kernel_version = models.CharField(max_length=255, null=False)
    cpu_cores = models.PositiveSmallIntegerField(null=True, blank=True)
    memory = models.PositiveSmallIntegerField(null=False) # GB 단위
    total_disk = models.PositiveSmallIntegerField(null=False) # GB 단위
    uptime = models.PositiveSmallIntegerField(null=False) # in days
    data_time = models.DateTimeField()
    comment = models.TextField(null=True, blank=True)

    cpu_usage = models.FloatField(null=True, blank=True) # CPU 사용률 (%)
    memory_usage = models.FloatField(null=True, blank=True) # Memory 사용률 (%)
    disk_usage = models.FloatField(null=True, blank=True) # Disk(/) 사용률 (%)
    
    is_virtual = models.BooleanField(default=True, null=False) # 가상서버여부
    is_master = models.BooleanField(default=True, null=False) # 마스터서버여부
    is_confirmed = models.BooleanField(default=False, null=False)
    
    run_time = models.DateTimeField(auto_now_add=True)
    
    @property
    def os_version_display(self):
        return self.os_version.replace('Red Hat Enterprise Linux', 'RHEL')

    def __str__(self) -> str:
        return f'{self.hostname}'
    
    class Meta:
        ordering = ['hostname','-data_time']