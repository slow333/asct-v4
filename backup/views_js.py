from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from ..asct.models_resource import CPUUsage
import json
from django.core.serializers.json import DjangoJSONEncoder
from django.utils import timezone
from datetime import timedelta

@login_required
def cpu_usage_chart(request):
    period = request.GET.get('period', '1m')
    query = request.GET.get('q', '')
    
    # Dropdown을 위한 호스트 목록 조회 (중복 제거)
    host_list = CPUUsage.objects.exclude(hostname__isnull=True).values_list('hostname', flat=True).distinct().order_by('hostname')
    
    # 날짜순으로 전체 데이터 조회
    queryset = CPUUsage.objects.all().order_by('data_time')
    
    if query:
        queryset = queryset.filter(hostname=query)
    
    if period == '1w':
        queryset = queryset.filter(data_time__gte=timezone.now() - timedelta(days=7))
    elif period == '1m':
        queryset = queryset.filter(data_time__gte=timezone.now() - timedelta(days=30))
    elif period == '3m':
        queryset = queryset.filter(data_time__gte=timezone.now() - timedelta(days=90))
    
    # 호스트별로 데이터 그룹화
    # datasets structure: { 'hostname': { label: 'hostname', data: [{x: time, y: value}, ...] } }
    grouped_data = {}
    for entry in queryset:
        host = entry.hostname
        if host not in grouped_data:
            grouped_data[host] = {
                'label': host,
                'data': [],
                'tension': 0.3, # 곡선 부드러움 정도
                'fill': False
            }
        grouped_data[host]['data'].append({
            'x': entry.data_time.isoformat(),
            'y': float(entry.usage_p)
        })

    context = {
        'datasets_json': json.dumps(list(grouped_data.values()), cls=DjangoJSONEncoder),
        'period': period,
        'query': query,
        'host_list': host_list
    }
    return render(request, 'asct/cpu_usage/chart.html', context)