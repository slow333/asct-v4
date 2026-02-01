from django import forms
from .models_basic import Command, SSHInfo, ServerInfo
from django.contrib.auth.models import User

class CommandForm(forms.ModelForm):
    class Meta:
        model= Command
        fields = ['name', 'script', 'description', 'category']
        verbose_name = '명령어'
        verbose_name_plural = '명령어들'
        labels = {
            'name': '이름',
            'script': '명령어',
            'description': '설명',
            'category': '분류',
        }
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control mb-2 fs-4', 
                'placeholder': '이름을 입력하세요', }),
            'script': forms.Textarea(attrs={
                'class': 'form-control text-muted mb-2', 
                'rows': '3',
                'placeholder': '명령어를 입력하세요',}),
            'description': forms.Textarea(attrs={
                'class': 'form-control text-muted mb-2', 
                'rows': '3',
                'placeholder': '설명을 입력하세요',}),
            'category': forms.Select(attrs={
                'class': 'form-select text-muted mb-2',}),
            }

class SSHInfoForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(SSHInfoForm, self).__init__(*args, **kwargs)
        self.fields['operators'].queryset = User.objects.all().order_by('username') # type: ignore

    class Meta:
        model= SSHInfo
        fields = ['name','login_id', 'ip', 'port', 'password', 'operators']
        labels = {
            'name': '이름',
            'login_id': '로그인 ID',
            'ip': '접속 IP',
            'port': '포트',
            'password': '암호',
        }
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control text-muted mb-2 fs-4', 
                'placeholder': '이름을 입력하세요', }),
            'login_id': forms.TextInput(attrs={
                'class': 'form-control text-muted mb-2', 
                'placeholder': '로그인 ID를 입력하세요', }),
            'ip': forms.TextInput(attrs={
                'class': 'form-control text-muted mb-2', 
                'placeholder': 'IP를 입력하세요',}),
            'port': forms.NumberInput(attrs={
                'class': 'form-control text-muted mb-2', 
                'placeholder': '포트를 입력하세요'}),
            'password': forms.TextInput(attrs={
                'class': 'form-control text-muted mb-2'}),
            'operators': forms.SelectMultiple(attrs={
                'class': 'form-select text-muted mb-2 select2'}),
            }

class ServerInfoForm(forms.ModelForm):
    class Meta:
        model = ServerInfo
        fields = ('hostname', 'ip1','ip2','os_version','kernel_version','cpu_cores', 'memory', 'total_disk', 'uptime', 'data_time', 'comment', 'is_virtual', 'is_master','is_confirmed')
        labels = {
            'memory': 'Memory(GB)',
            'total_disk': 'Total Disk Size(GB)',
            'uptime': 'uptime(days)',
        }
        widgets = {
            "hostname": forms.TextInput(attrs={"class": "form-control", "style": "width: 100%;", "placeholder": "hostname"}),
            "ip1": forms.TextInput(attrs={"class": "form-control", "style": "width: 100%;", "placeholder": "ip1"}),
            "ip2": forms.TextInput(attrs={"class": "form-control", "style": "width: 100%;", "placeholder": "ip2"}),
            "os_version": forms.TextInput(attrs={"class": "form-control", "style": "width: 100%;", "placeholder": "os_version"}),
            "kernel_version": forms.TextInput(attrs={"class": "form-control", "style": "width: 100%;", "placeholder": "kernel_version"}),
            "cpu_cores": forms.NumberInput(attrs={"class": "form-control", "style": "width: 100%;", "placeholder": "cpu_cores"}),
            "memory": forms.NumberInput(attrs={"class": "form-control", "style": "width: 100%;", "placeholder": "memory size"}),
            "total_disk": forms.NumberInput(attrs={"class": "form-control", "style": "width: 100%;", "placeholder": "NumberInput"}),
            "uptime": forms.NumberInput(attrs={"class": "form-control", "style": "width: 100%;", "placeholder": "uptime(days)"}),
            "data_time": forms.DateTimeInput(attrs={"class": "form-control", "style": "width: 100%;", "placeholder": "data_time"}),
            "comment": forms.Textarea(attrs={"class": "form-control", "style": "width: 100%;", "rows":'3', "placeholder": "comment"}),
            
            "is_virtual": forms.CheckboxInput(attrs={"class": "form-check-input", }),
            "is_master": forms.CheckboxInput(attrs={"class": "form-check-input",}),
            "is_confirmed": forms.CheckboxInput(attrs={"class": "form-check-input",}),
        }