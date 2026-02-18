import matplotlib
import re
matplotlib.use('Agg') # 웹 서버에서 Matplotlib을 사용하기 위한 설정
import matplotlib.pyplot as plt
import io
import base64
from django.shortcuts import render
from .models import ServerInfo
from django.db.models import Count
from .views_common import buffered_img
from django.http import JsonResponse
from config.celery import app

def dashboard(request):
    servers = ServerInfo.objects.all()
    
    # 1. OS 버전별 분포 (Pie Chart용)
    os_dist = servers.values('os_version').annotate(count=Count('os_version')).order_by('-count')
    # 2. Memory 상위 10개 서버 (Bar Chart용)
    top_memory = servers.order_by('-memory')[:10]
    # 3. Disk 상위 10개 서버 (Bar Chart용)
    top_disk = servers.order_by('-total_disk')[:10]
    # 4. Resource Usage Top 5 (Progress Bar용)
    top_cpu_usage = servers.exclude(cpu_usage__isnull=True).order_by('-cpu_usage')[:5]
    top_memory_usage = servers.exclude(memory_usage__isnull=True).order_by('-memory_usage')[:5]
    top_disk_usage = servers.exclude(disk_usage__isnull=True).order_by('-disk_usage')[:5]
    
    # 차트 생성을 위한 데이터 (뷰에서 이 데이터를 준비해야 합니다)
    os_labels = list(os_dist.values_list('os_version', flat=True))
    labels_replace = [ re.sub(r'\s*\([^)]*\)', '', l)
                    .strip().replace('Red Hat Enterprise Linux', 'RHEL')
                    .replace('Server ', '')
                    .replace(' release', '') for l in os_labels ]
    os_data = list(os_dist.values_list('count', flat=True))
    mem_labels = [s.hostname for s in top_memory]
    mem_data = [s.memory for s in top_memory]
    disk_labels = [s.hostname for s in top_disk]
    disk_data = [s.total_disk for s in top_disk]
    # --- 데이터 준비 끝 ---

    # 1. OS 분포 차트 (파이 차트)
    os_chart = None
    if os_data:
        fig_os, ax_os = plt.subplots(figsize=(6, 6))
        ax_os.pie(os_data, labels=labels_replace, autopct='%1.1f%%', startangle=90, textprops={'fontsize': 16})
        ax_os.axis('equal')  # 파이 차트를 원형으로 만듭니다.
        os_chart = buffered_img(fig_os)

    # 2. 메모리 상위 서버 차트 (바 차트)
    memory_chart = None
    if mem_data:
        fig_mem, ax_mem = plt.subplots(figsize=(6, 4))
        ax_mem.bar(mem_labels, mem_data, color='royalblue')
        ax_mem.set_ylabel('Memory (GB)', fontsize=14)
        ax_mem.set_title('Top Memory Servers', fontsize=16)
        ax_mem.tick_params(axis='both', labelsize=14)
        plt.setp(ax_mem.get_xticklabels(), rotation=45, ha="right")
        memory_chart = buffered_img(fig_mem)

    # 3. 디스크 상위 서버 차트 (바 차트)
    disk_chart = None
    if disk_data:
        fig_disk, ax_disk = plt.subplots(figsize=(6, 4))
        ax_disk.bar(disk_labels, disk_data, color='teal')
        ax_disk.set_ylabel('Total Disk (GB)', fontsize=14)
        ax_disk.set_title('Top Disk Servers', fontsize=16)
        ax_disk.tick_params(axis='both', labelsize=14)
        plt.setp(ax_disk.get_xticklabels(), rotation=45, ha="right")
        disk_chart = buffered_img(fig_disk)

    context = {
        'total_servers': servers.count(),
        'virtual_count': servers.filter(is_virtual=True).count(),
        'physical_count': servers.filter(is_virtual=False).count(),
        'top_cpu_usage': top_cpu_usage,
        'top_memory_usage': top_memory_usage,
        'top_disk_usage': top_disk_usage,
        'os_chart': os_chart,
        'memory_chart': memory_chart,
        'disk_chart': disk_chart,
    }
    
    return render(request, 'asct/dashboard.html', context)

def check_celery_status(request):
    try:
        # Celery Worker 상태 확인 (Timeout 1.0초)
        inspector = app.control.inspect(timeout=1.0)
        
        # Worker Ping (응답 없으면 None)
        workers = inspector.ping()
        
        if not workers:
            return JsonResponse({
                'status': 'error', 
                'message': 'No Celery Workers found.'
            }, status=503)
        
        # 현재 실행 중인 태스크 정보 조회
        active_tasks = inspector.active()
        
        return JsonResponse({
            'status': 'running',
            'workers': list(workers.keys()),
            'active_tasks': active_tasks
        })
        
    except Exception as e:
        return JsonResponse({
            'status': 'error', 
            'message': str(e)
        }, status=500)
