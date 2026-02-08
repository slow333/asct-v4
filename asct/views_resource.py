from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.http import HttpResponse
from .models_resource import CPUUsage, MemoryUsage, NetworkUsage
from .models_basic import SSHInfo
from .run_by_ssh import run_ssh_cpu_usage, run_ssh_memory_usage, run_ssh_traffic_usage
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
    if period == '1w':
        queryset = queryset.filter(data_time__gte=timezone.now() - timedelta(days=7))
    elif period == '1m':
        queryset = queryset.filter(data_time__gte=timezone.now() - timedelta(days=30))
    elif period == '3m':
        queryset = queryset.filter(data_time__gte=timezone.now() - timedelta(days=90))
    return queryset, period

def filter_by_q_and_hostlist(request, model_obj):
    queryset = model_obj.objects.all().order_by('data_time')
    host_list = model_obj.objects.exclude(hostname__isnull=True).values_list('hostname', flat=True).distinct().order_by('hostname')
    
    query = request.GET.get('q', '')
    if query:
        queryset = model_obj.objects.filter(hostname=query)
    else:
        queryset = model_obj.objects.all()
    
    return queryset, query, host_list

def buffered_image(fig):
    buffer = io.BytesIO()
    fig.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    buffer.close()
    plt.close(fig)
    
    return image_png

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
    
    queryset = model_class.objects.all().order_by('hostname', '-data_time')
    for obj in queryset:
        data_time_val = obj.data_time.replace(tzinfo=None) if obj.data_time else ''
        ws.append(row_mapper(obj, data_time_val)) # type: ignore
        
    wb.save(response)
    return response

def common_chart(request, model_class, title_prefix, y_label, data_extractor, template_name):
    queryset, query, host_list = filter_by_q_and_hostlist(request, model_class)
    queryset, period = filter_by_days(request, queryset)
    
    fig, ax = plt.subplots(figsize=(12, 6))
    
    data_map = {}
    for entry in queryset:
        for label, value in data_extractor(entry):
            if label not in data_map: 
                data_map[label] = {'x': [], 'y': []}
            data_map[label]['x'].append(entry.data_time)
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
    
    image_png = buffered_image(fig)
    graphic = base64.b64encode(image_png).decode('utf-8')
    
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

# =============== Traffic usage 관련 CRUD ===============
@login_required
def traffic_usage_select(request):
    return common_usage_select(request, 'asct:traffic_usage_run', 'asct/traffic_usage/select.html')

@login_required
def traffic_usage_run(request, ssh_id):
    ssh_info = get_object_or_404(SSHInfo, id=ssh_id)
    _, _, data, error = run_ssh_traffic_usage(request, ssh_info)
    
    if error:
        messages.error(request, f"Error: {error}")
    else:
        messages.success(request, f"Successfully collected {data.get('count', 0)} records.")
    return redirect('asct:traffic_usage_list')

@login_required
def traffic_usage_list(request):
    return common_list(request, NetworkUsage, 'asct/traffic_usage/list.html')

@login_required
def traffic_usage_export(request):
    headers = ['Hostname', 'IP', 'Date Time', 'Interface', 'Speed', 'RX(kB/s)', 'TX(kB/s)', 'Confirmed', 'Comment']
    
    def mapper(obj, dt_val):
        return [
            obj.hostname, obj.ip, dt_val, obj.if_name, obj.speed, 
            obj.rxkB_s, obj.txkB_s, 
            "Yes" if obj.is_confirmed else "No", obj.comment
        ]
        
    return common_export("traffic_usage_list.xlsx", "Traffic Usage", headers, NetworkUsage, mapper)

@login_required
def traffic_usage_chart(request):
    def extractor(entry):
        return [
            (f"{entry.hostname} - {entry.if_name} (RX)", entry.rxkB_s),
            (f"{entry.hostname} - {entry.if_name} (TX)", entry.txkB_s)
        ]
    return common_chart(request, NetworkUsage, 'Traffic Usage', 'Speed (kB/s)', extractor, 'asct/traffic_usage/chart.html')

# =============== Memory usage 관련 CRUD ===============
@login_required
def memory_usage_list(request):
    return common_list(request, MemoryUsage, 'asct/memory_usage/list.html')

@login_required
def memory_usage_chart(request):
    def extractor(entry):
        return [(entry.hostname, entry.usage_p)]
    return common_chart(request, MemoryUsage, 'Memory Usage', 'Usage (%)', extractor, 'asct/memory_usage/chart.html')

@login_required
def memory_usage_select(request):
    return common_usage_select(request, 'asct:memory_usage_run', 'asct/memory_usage/select.html')

@login_required
def memory_usage_run(request, ssh_id):
    ssh_info = get_object_or_404(SSHInfo, id=ssh_id)
    _, _, data, error = run_ssh_memory_usage(request, ssh_info)
    
    if error:
        messages.error(request, f"Error: {error}")
    else:
        messages.success(request, f"Successfully collected {data.get('count', 0)} records.")
    return redirect('asct:memory_usage_list')

@login_required
def memory_usage_export(request):
    headers = ['Hostname', 'IP', 'Date Time', 'Total Memory(MB)', 'Usage(%)', 'Confirmed', 'Comment']
    
    def mapper(obj, dt_val):
        return [
            obj.hostname, obj.ip, dt_val, obj.total_memory, obj.usage_p,
            "Yes" if obj.is_confirmed else "No", obj.comment
        ]
        
    return common_export("memory_usage_list.xlsx", "Memory Usage", headers, MemoryUsage, mapper)

# =============== CPU usage 관련 CRUD ===============
@login_required
def cpu_usage_list(request):
    return common_list(request, CPUUsage, 'asct/cpu_usage/list.html')

@login_required
def cpu_usage_chart(request):
    def extractor(entry):
        return [(entry.hostname, entry.usage_p)]
    return common_chart(request, CPUUsage, 'CPU Usage', 'Usage (%)', extractor, 'asct/cpu_usage/chart.html')

# =============== Paramiko 실행 예시 ===============
@login_required
def cpu_usage_select(request):
    return common_usage_select(request, 'asct:cpu_usage_run', 'asct/cpu_usage/select.html')

@login_required
def cpu_usage_run(request, ssh_id):
    ssh_info = get_object_or_404(SSHInfo, id=ssh_id)
    _, _, data, error = run_ssh_cpu_usage(request, ssh_info)
    
    if error:
        messages.error(request, f"Error: {error}")
    else:
        messages.success(request, f"Successfully collected {data.get('count', 0)} records.")
        
    return redirect('asct:cpu_usage_list')

@login_required
def cpu_usage_export(request):
    headers = ['Hostname', 'IP', 'Date Time', 'CPU Cores', 'Usage(%)', 'Confirmed', 'Comment']
    
    def mapper(obj, dt_val):
        return [
            obj.hostname, obj.ip, dt_val, obj.cpu_cores, obj.usage_p,
            "Yes" if obj.is_confirmed else "No", obj.comment
        ]
        
    return common_export("cpu_usage_list.xlsx", "CPU Usage", headers, CPUUsage, mapper)