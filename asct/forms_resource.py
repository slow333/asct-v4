from django import forms
from .models_resource import CPUUsage
from django.contrib.auth.models import User

class CPUUsageForm(forms.ModelForm):
    class Meta:
        model= CPUUsage
        fields = ['ssh_info','hostname', 'ip', 'cpu_cores', 'usage_p','data_time', 'comment', 'is_confirmed']
