from django.db import models
from .models_basic import SSHInfo

class CPUUsage(models.Model):
    ssh_info = models.ForeignKey(SSHInfo, on_delete=models.CASCADE)
    hostname = models.CharField(max_length=50, null=True)
    ip = models.GenericIPAddressField(default="127.0.0.0", null=False)
    cpu_cores = models.PositiveSmallIntegerField(default=1, null=False)
    usage_p = models.DecimalField(max_digits=8, decimal_places=2)
    data_time = models.DateTimeField()
    
    comment = models.TextField(null=True, blank=True)
    is_confirmed = models.BooleanField(default=False, null=False)
    
    @property
    def cpu_core_count(self):
        return self.cpu_cores
    
    def __str__(self) -> str:
        return f'CPU Usage : {self.hostname} => {self.usage_p}'
    
    class Meta:
        ordering = ['hostname','-data_time']
        unique_together = ('hostname','ip','data_time')

class MemoryUsage(models.Model):
    ssh_info = models.ForeignKey(SSHInfo, on_delete=models.CASCADE)
    hostname = models.CharField(max_length=50, null=True)
    ip = models.GenericIPAddressField(default="127.0.0.0", null=False)
    total_memory = models.PositiveIntegerField(default=0, null=False) # MB 단위
    usage_p = models.DecimalField(max_digits=5, decimal_places=2)
    data_time = models.DateTimeField()
    
    comment = models.TextField(null=True, blank=True)
    is_confirmed = models.BooleanField(default=False, null=False)
    
    def __str__(self) -> str:
        return f'Memory Usage : {self.hostname} => {self.usage_p}%'
    
    class Meta:
        ordering = ['hostname','-data_time']
        unique_together = ('hostname','ip','data_time')

class NetworkUsage(models.Model):
    ssh_info = models.ForeignKey(SSHInfo, on_delete=models.CASCADE)
    
    hostname = models.CharField(max_length=50, null=True)
    ip = models.GenericIPAddressField(default="127.0.0.0", null=False)
    if_name = models.CharField(max_length=20, default='eth0', null=False)
    speed = models.CharField(max_length=10, default='1G', null=False)
    rxkB_s = models.DecimalField(max_digits=20, decimal_places=2, null=False)
    txkB_s = models.DecimalField(max_digits=20, decimal_places=2, null=False)
    data_time = models.DateTimeField(null=False)
    
    comment = models.TextField(null=True, blank=True)
    is_confirmed = models.BooleanField(default=False)
    
    def __str__(self) -> str:
        return f'Network Usage : {self.hostname} => {self.rxkB_s} per second , {self.txkB_s} per second'
    
    class Meta:
        ordering = ['hostname','-data_time']
        unique_together = ('hostname','ip', 'data_time')

class DiskUsage(models.Model):
    ssh_info = models.ForeignKey(SSHInfo, on_delete=models.CASCADE)
    
    hostname = models.CharField(max_length=50, null=True)
    ip = models.GenericIPAddressField(default="127.0.0.0", null=False)
    
    device = models.CharField(max_length=255, default='/dev')
    mounted = models.CharField(max_length=255, default='/')
    size = models.FloatField(null=False, default=0.0) 
    use_p = models.IntegerField(null=False, default=0)
    checked_at = models.DateTimeField(auto_now_add=True)
    
    comment = models.TextField(null=True, blank=True)
    is_confirmed = models.BooleanField(default=False)
    
    def __str__(self) -> str:
        return f'Disk Usage for {self.hostname}'
    
    class Meta:
        ordering = ['hostname','-checked_at']
        unique_together = ('hostname','ip', 'checked_at')


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