from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from django.http import HttpResponse
from .models_basic import SSHInfo
import openpyxl
from django.utils import timezone
from datetime import timedelta
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import io
import base64

# ================= common def ==================
def filter_by_days(request, queryset):
    period = request.GET.get('period', '1m')
    
    date_field = 'data_time'
    if hasattr(queryset.model, 'checked_at'):
        date_field = 'checked_at'

    if period == '1w':
        queryset = queryset.filter(**{f'{date_field}__gte': timezone.now() - timedelta(days=7)})
    elif period == '1m':
        queryset = queryset.filter(**{f'{date_field}__gte': timezone.now() - timedelta(days=30)})
    elif period == '3m':
        queryset = queryset.filter(**{f'{date_field}__gte': timezone.now() - timedelta(days=90)})
    return queryset, period

def filter_by_q_and_hostlist(request, model_obj):
    queryset = model_obj.objects.all()
    host_list = model_obj.objects.exclude(hostname__isnull=True).values_list('hostname', flat=True).distinct().order_by('hostname')
    
    query = request.GET.get('q', '')
    if query:
        queryset = queryset.filter(hostname=query)

    if hasattr(model_obj, 'data_time'):
        queryset = queryset.order_by('data_time')
    elif hasattr(model_obj, 'checked_at'):
        queryset = queryset.order_by('checked_at')

    return queryset, query, host_list

# 차트를 생성하고 base64로 인코딩하는 헬퍼 함수
# 참고: 차트에 한글을 사용하려면 시스템에 맞는 한글 폰트를 설정해야 합니다.
# 예: plt.rcParams['font.family'] = 'Malgun Gothic'
def buffered_img(fig):
    buffer = io.BytesIO()
    fig.savefig(buffer, format='png', bbox_inches='tight')
    buffer.seek(0)
    image_base64 = base64.b64encode(buffer.read()).decode('utf-8')
    buffer.close()
    plt.rcParams['font.family'] = 'Malgun Gothic'
    plt.close(fig)
    return image_base64

def common_usage_select(request, run_url_name, template_name):
    if request.method == 'POST':
        ssh_id = request.POST.get('ssh_id')
        if ssh_id:
            return redirect(run_url_name, ssh_id=ssh_id)
    sshinfos = SSHInfo.objects.filter(operators=request.user)
    return render(request, template_name, {'sshinfos': sshinfos})

def common_export(filename, sheet_title, headers, model_class, row_mapper):
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = sheet_title # type: ignore
    ws.append(headers) # type: ignore
    
    date_field = 'data_time'
    if hasattr(model_class, 'checked_at'):
        date_field = 'checked_at'

    queryset = model_class.objects.all().order_by('hostname', f'-{date_field}')
    for obj in queryset:
        dt = getattr(obj, date_field)
        data_time_val = dt.replace(tzinfo=None) if dt else ''
        ws.append(row_mapper(obj, data_time_val)) # type: ignore
        
    wb.save(response)
    return response

def common_chart(request, model_class, title_prefix, y_label, data_extractor, template_name):
    queryset, query, host_list = filter_by_q_and_hostlist(request, model_class)
    queryset, period = filter_by_days(request, queryset)

    date_field = 'data_time'
    if hasattr(model_class, 'checked_at'):
        date_field = 'checked_at'

    fig, ax = plt.subplots(figsize=(12, 6))

    data_map = {}
    for entry in queryset:
        for label, value in data_extractor(entry):
            if label not in data_map: 
                data_map[label] = {'x': [], 'y': []}
            data_map[label]['x'].append(getattr(entry, date_field))
            data_map[label]['y'].append(float(value))

    for label, data in data_map.items():
        ax.plot(data['x'], data['y'], label=label, marker='o', markersize=3)
        
    ax.set_title(f'{title_prefix} ({period})')
    ax.set_xlabel('Date Time')
    ax.set_ylabel(y_label)
    
    if 0 < len(data_map) < 20:
        ax.legend()

    ax.grid(True)
    fig.tight_layout()
    
    graphic = buffered_img(fig)
    # graphic = base64.b64encode(image_png).decode('utf-8')
    
    context = {
        'chart_graphic': graphic,
        'period': period,
        'query': query,
        'host_list': host_list
    }
    return render(request, template_name, context)

def common_list(request, model_class, template_name):
    queryset, query, host_list = filter_by_q_and_hostlist(request, model_class)
    
    paginator = Paginator(queryset, 10)
    page = request.GET.get("page")
    page_obj = paginator.get_page(page)
    
    return render(request, template_name, {'page_obj': page_obj, 'query': query, 'host_list': host_list})
