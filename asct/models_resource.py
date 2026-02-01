from django.db import models
from django.contrib.auth.models import User


# class CPUUsage(models.Model):
#     serverinfo = models.OneToOneField(ServerInfo, on_delete=models.CASCADE)
    
#     usage_percent = models.DecimalField(max_digits=8, decimal_places=2, null=False)
#     data_time = models.DateTimeField(null=False)
    
#     comment = models.TextField(null=True, blank=True)
#     is_confirmed = models.BooleanField(default=False, null=False)
    
#     def cpu_core_count(self):
#         return self.serverinfo.cpu_cores
    
#     def __str__(self) -> str:
#         return f'CPU Usage for {self.serverinfo.hostname}'
    
#     class Meta:
#         ordering = ['serverinfo__hostname','-data_time']
#         unique_together = ('serverinfo','data_time')

# class MemoryUsage(models.Model):
#     serverinfo = models.OneToOneField(ServerInfo, on_delete=models.CASCADE)
    
#     usage_percent = models.DecimalField(max_digits=4, decimal_places=2, null=False)
#     @property
#     def total_memory(self):
#         return self.serverinfo.memory
#     data_time = models.DateTimeField(null=False)
    
#     comment = models.TextField(null=True, blank=True)
#     is_confirmed = models.BooleanField(default=False, null=False)
    
#     def __str__(self) -> str:
#         return f'Memory Usage for {self.serverinfo.hostname}'
    
#     class Meta:
#         ordering = ['serverinfo__hostname','-data_time']
#         unique_together = ('serverinfo', 'data_time')

# class DiskUsage(models.Model):
#     serverinfo = models.OneToOneField(ServerInfo, on_delete=models.CASCADE)
    
#     storage_local_total = models.IntegerField(null=False) 
#     storage_local_usage_percent = models.DecimalField(max_digits=4, decimal_places=2, null=False)
#     data_time = models.DateTimeField(null=False)
    
#     comment = models.TextField(null=True, blank=True)
#     is_confirmed = models.BooleanField(default=False, null=False)
    
#     def __str__(self) -> str:
#         return f'Disk Usage for {self.serverinfo.hostname}'
    
#     class Meta:
#         ordering = ['serverinfo__hostname','-data_time']
#         unique_together = ('serverinfo', 'data_time')

# class NetworkUsage(models.Model):
#     serverinfo = models.OneToOneField(ServerInfo, on_delete=models.CASCADE)
    
#     network_type = [
#         ('100M','100M'),('1G','1G'), ('10G','10G'), ('40G','40G'), ('100G','100G'), 
#         ('8G','8G FC'), ('16G','16G FC'), ('32G','32G FC'), ('64G','64G FC')]
#     network_service = models.CharField(max_length=10, choices=network_type, default='1G', null=False)
#     in_bytes = models.DecimalField(max_digits=20, decimal_places=2, null=False)
#     out_bytes = models.DecimalField(max_digits=20, decimal_places=2, null=False)
#     data_time = models.DateTimeField(null=False)
    
#     comment = models.TextField(null=True, blank=True)
#     is_confirmed = models.BooleanField(default=False)
    
#     def __str__(self) -> str:
#         return f'Network Usage for {self.serverinfo.hostname}'
    
#     class Meta:
#         ordering = ['serverinfo__hostname','-data_time']
#         unique_together = ('serverinfo', 'data_time')

# class SysctlSetting(models.Model):
#     serverinfo = models.OneToOneField(ServerInfo, on_delete=models.CASCADE)
    
#     name = models.CharField(max_length=255, unique=True, null=False)
#     description = models.TextField(null=True, blank=True)
#     value = models.CharField(max_length=255, null=False)
    
#     data_time =models.DateTimeField(auto_now=True)
#     comment = models.TextField(null=True, blank=True)
#     is_confirmed = models.BooleanField(default=False, null=False)
    
#     def __str__(self) -> str:
#         return f'Sysctl {self.name} for {self.serverinfo.hostname}'
    
#     class Meta:
#         ordering = ['serverinfo','-data_time']

# class SystemLog(models.Model):
#     serverinfo = models.ForeignKey(ServerInfo, on_delete=models.PROTECT)
    
#     log_level_choices = [
#         ('DEBUG','DEBUG'),('INFO','INFO'), ('WARNING','WARNING'), ('ERROR','ERROR'), ('CRITICAL','CRITICAL')]
    
#     log_level = models.CharField(max_length=10, choices=log_level_choices, null=False, default='ERROR')
#     messages = models.TextField(null=True, blank=True)
    
#     data_time = models.DateTimeField(auto_now=True)
#     comment = models.TextField(null=True, blank=True)
#     is_confirmed = models.BooleanField(default=False, null=False)
    
#     def save(self, *args, **kwargs):
#         # 개발시는 전체 저장
#         if any(level in self.log_message.lower() for level in ['error', 'info', 'warning', 'critical', 'debug']): # type: ignore
#             super().save(*args, **kwargs)
#         # 'error' 또는 'info'가 없으면 아무 작업도 하지 않아 저장을 건너뜁니다.

#     def __str__(self) -> str:
#         return f'Log from {self.serverinfo.hostname} at {self.data_time}'

#     class Meta:
#         ordering = ['serverinfo','-data_time']
#         unique_together = ('serverinfo', 'data_time')

class Command(models.Model):
    CATEGORY = (
        ('os', 'Operatiion System Command'),
        ('basic', 'Basic Shell Command'),
        ('app','Application Command'),
        ('traffic','Traffic Command'),
        ('sysctl','System ctl Command'),
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
