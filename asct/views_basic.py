from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.conf import settings
from django.db.models import Count
from django.http import HttpResponse
from .models_basic import Command, SSHInfo, CommandHistory, ServerInfo
from .forms_basic import CommandForm, SSHInfoForm, ServerInfoForm
import paramiko
import os
import json
import openpyxl

def index(request):
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

    context = {
        'total_servers': servers.count(),
        'virtual_count': servers.filter(is_virtual=True).count(),
        'physical_count': servers.filter(is_virtual=False).count(),
        'os_labels': list(os_dist.values_list('os_version', flat=True)),
        'os_data': list(os_dist.values_list('count', flat=True)),
        'mem_labels': [s.hostname for s in top_memory],
        'mem_data': [s.memory for s in top_memory],
        'disk_labels': [s.hostname for s in top_disk],
        'disk_data': [s.total_disk for s in top_disk],
        'top_cpu_usage': top_cpu_usage,
        'top_memory_usage': top_memory_usage,
        'top_disk_usage': top_disk_usage,
    }
    return render(request, 'asct/dashboard.html', context)

# =============== command 관련 CRUD ===============
def cmd_list(request):
    commands = Command.objects.all()
    
    category_list = []
    for key, value in Command.CATEGORY:
        category_list.append({
            'category': key,
            'name': value,
            'count': Command.objects.filter(category=key).count()
        })
    current_category = request.GET.get('category')

    if current_category:
        commands = commands.filter(category=current_category)
    
    pagenator = Paginator(commands, 10)
    page = request.GET.get("page")
    page_obj = pagenator.get_page(page)
    
    return render(request, 'asct/command/list.html', {'page_obj': page_obj, 'current_category': current_category, 'category_list':category_list})

def cmd_add(request):
    if request.method == 'POST':
        form = CommandForm(data=request.POST)
        if form.is_valid:
            form.save()
            return redirect('asct:command_list')
    form = CommandForm()
    return render(request, 'asct/command/add.html', {'form': form})

def cmd_detail(request, pk):
    command = get_object_or_404(Command, id = pk)
    
    return render(request, 'asct/command/detail.html', {'command': command})

def cmd_update(request, pk):
    command = get_object_or_404(Command, id = pk)
    if request.method == 'POST':
        form = CommandForm(data=request.POST, instance=command)
        if form.is_valid:
            form.save()
            return redirect('asct:command_detail', pk)
    form = CommandForm(instance=command)
    return render(request, 'asct/command/update.html', {'form': form})

def cmd_delete(request, pk):
    command = get_object_or_404(Command, id = pk)
    Command.delete(command)
    return redirect('asct:command_list')

# =============== sshifo 관련 CRUD ===============
@login_required
def sshinfo_list(request):
    sshinfos = SSHInfo.objects.all().order_by('name')
    
    pagenator = Paginator(sshinfos, 10)
    page = request.GET.get("page")
    page_obj = pagenator.get_page(page)
    
    return render(request, 'asct/sshinfo/list.html', {'page_obj': page_obj})

@login_required
def sshinfo_add(request):
    if request.method == 'POST':
        form = SSHInfoForm(data=request.POST)
        if form.is_valid:
            form.save()
            return redirect('asct:sshinfo_list')
    form = SSHInfoForm()
    return render(request, 'asct/sshinfo/add.html', {'form': form})

@login_required
def sshinfo_detail(request, pk):
    sshinfo = get_object_or_404(SSHInfo, id = pk)
    
    return render(request, 'asct/sshinfo/detail.html', {'sshinfo': sshinfo})

@login_required
def sshinfo_update(request, pk):
    sshinfo = get_object_or_404(SSHInfo, id = pk)
    if request.method == 'POST':
        form = SSHInfoForm(data=request.POST, instance=sshinfo)
        if form.is_valid:
            form.save()
            return redirect('asct:sshinfo_detail', pk)
    form = SSHInfoForm(instance=sshinfo)
    return render(request, 'asct/sshinfo/update.html', {'form': form})

@login_required
def sshinfo_delete(request, pk):
    sshinfo = get_object_or_404(SSHInfo, id = pk)
    SSHInfo.delete(sshinfo)
    return redirect('asct:sshinfo_list')

# =============== Paramiko 실행 예시 ===============
@login_required
def cmd_history_list(request):
    histories = CommandHistory.objects.all()
    
    paginator = Paginator(histories, 15)
    page = request.GET.get("page")
    page_obj = paginator.get_page(page)
    
    return render(request, 'asct/run/history_list.html', {'page_obj': page_obj})

@login_required
def cmd_history_delete(request, pk):
    history = CommandHistory.objects.get(id = pk)
    CommandHistory.delete(history)
    return redirect('asct:command_history_list')
    
@login_required
def cmd_select(request):
    if request.method == 'POST':
        ssh_id = request.POST.get('ssh_id')
        cmd_id = request.POST.get('cmd_id')
        if ssh_id and cmd_id:
            return redirect('asct:run_command', ssh_id=ssh_id, cmd_id=cmd_id)

    commands = Command.objects.all()
    # 현재 로그인한 사용자가 권한을 가진 서버만 조회
    sshinfos = SSHInfo.objects.filter(operators=request.user)
    
    return render(request, 'asct/run/select.html', {'commands': commands, 'sshinfos': sshinfos})

@login_required
def run_cmd(request, ssh_id, cmd_id):
    ssh_info = get_object_or_404(SSHInfo, id=ssh_id)
    command_obj = get_object_or_404(Command, id=cmd_id)
    
    result = ""
    error = ""
    
    try:
        # 1. SSH 클라이언트 생성
        client = paramiko.SSHClient()
        # 2. 호스트 키 정책 설정 (알려지지 않은 호스트도 자동 허용 - 보안상 주의 필요)
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        # 3. 서버 접속
        client.connect(
            hostname=ssh_info.ip,
            port=ssh_info.port,
            username=ssh_info.login_id,
            password=ssh_info.password,
            timeout=10
        )
        
        # 4. 명령어 실행
        stdin, stdout, stderr = client.exec_command(command_obj.script)
        
        # 5. 결과 읽기 (bytes를 utf-8로 디코딩)
        result = stdout.read().decode('utf-8')
        error = stderr.read().decode('utf-8')
        
        client.close()
        
    except Exception as e:
        error = f"Connection Failed: {str(e)}"

    # 6. 실행 이력 저장
    CommandHistory.objects.create(
        ssh_info=ssh_info,
        command=command_obj,
        executed_by=request.user,
        stdout=result,
        stderr=error
    )

    # 결과를 보여줄 템플릿으로 렌더링 (result.html은 예시입니다)
    context = {
        'ssh_info': ssh_info,
        'command': command_obj,
        'result': result,
        'error': error,
    }
    return render(request, 'asct/run/result.html', context)

# =============== Paramiko server info 수집 ===============
@login_required
def serverinfo_list(request):
    serverinfos = ServerInfo.objects.all().order_by('hostname')
    
    paginator = Paginator(serverinfos, 15)
    page = request.GET.get("page")
    page_obj = paginator.get_page(page)
    
    return render(request, 'asct/svinfo/list.html', {'page_obj': page_obj})

@login_required
def serverinfo_export(request):
    # 1. 응답 객체 생성 (Excel 파일 설정)
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename="server_info_list.xlsx"'

    # 2. 워크북 및 워크시트 생성
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Server Info" # type: ignore

    # 3. 헤더 작성
    headers = ['Hostname', 'IP1', 'IP2', 'OS Version', 'Kernel', 'CPU Cores', 'CPU(%)', 'Memory(GB)', 'Mem(%)', 'Disk(GB)', 'Disk(%)', 'Uptime(days)', 'Last Updated']
    ws.append(headers) # type: ignore

    # 4. 데이터 작성
    servers = ServerInfo.objects.all().order_by('hostname')
    for server in servers:
        # Timezone 정보가 있는 datetime은 Excel 호환성을 위해 tzinfo 제거
        data_time_val = server.data_time.replace(tzinfo=None) if server.data_time else ''
        
        ws.append([ # type: ignore
            server.hostname,
            server.ip1,
            server.ip2,
            server.os_version_display,
            server.kernel_version,
            server.cpu_cores,
            server.cpu_usage,
            server.memory,
            server.memory_usage,
            server.total_disk,
            server.disk_usage,
            server.uptime,
            data_time_val
        ])

    # 5. 저장 및 반환
    wb.save(response)
    return response
from django.views.decorators.http import require_POST
@require_POST
@login_required
def serverinfo_update(request, pk):
    server_info = get_object_or_404(ServerInfo, id=pk)
    # if request.method == 'POST':
        if 'refresh_server' in request.POST:
            ssh_info = server_info.sshinfos
            if not ssh_info:
                messages.error(request, "No SSH Info associated with this server.")
                return redirect('asct:serverinfo_update', pk=pk)
            
            try:
                # 1. SSH Connection
                client = paramiko.SSHClient()
                client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                client.connect(
                    hostname=ssh_info.ip,
                    port=ssh_info.port,
                    username=ssh_info.login_id,
                    password=ssh_info.password,
                    timeout=10
                )
                
                # 2. Script Preparation & Upload
                script_path = os.path.join(settings.BASE_DIR, 'static', 'script_files', 'get_svinfo.sh')
                if not os.path.exists(script_path):
                    raise FileNotFoundError("Default script file not found.")
                
                sftp = client.open_sftp()
                remote_script = f'/tmp/get_svinfo_{ssh_info.id}.sh' # type: ignore
                sftp.put(script_path, remote_script)
                sftp.chmod(remote_script, 0o755)
                sftp.close()
                
                # 3. Execute Script (Fix windows line endings first)
                client.exec_command(f"sed -i 's/\r$//' {remote_script}")
                
                stdin, stdout, stderr = client.exec_command(remote_script)
                exit_status = stdout.channel.recv_exit_status()
                output = stdout.read().decode('utf-8')
                err_output = stderr.read().decode('utf-8')
                
                # 4. Cleanup
                client.exec_command(f"rm {remote_script}")
                client.close()
                
                if exit_status == 0:
                    # 5. Parse & Update
                    json_str = output[output.find('{'):output.rfind('}')+1]
                    data = json.loads(json_str)
                    
                    server_info.hostname = data['hostname']
                    server_info.ip1 = data.get('ip1')
                    server_info.ip2 = data.get('ip2')
                    server_info.os_version = data.get('os_version')
                    server_info.kernel_version = data.get('kernel_version')
                    server_info.cpu_cores = data.get('cpu_cores')
                    server_info.memory = data.get('memory')
                    server_info.total_disk = data.get('total_disk')
                    server_info.uptime = data.get('uptime')
                    server_info.data_time = data.get('data_time')
                    server_info.is_virtual = data.get('is_virtual')
                    server_info.cpu_usage = data.get('cpu_usage')
                    server_info.memory_usage = data.get('memory_usage')
                    server_info.disk_usage = data.get('disk_usage')
                    server_info.save()
                    
                    messages.success(request, f"Successfully refreshed info for {server_info.hostname}")
                else:
                    messages.error(request, f"Script execution failed: {err_output}")
            except Exception as e:
                messages.error(request, f"Error refreshing info: {str(e)}")
            
            return redirect('asct:serverinfo_update', pk=pk)

        form = ServerInfoForm(request.POST, instance=server_info)
        if form.is_valid():
            form.save()
            return redirect('asct:serverinfo_list')
    else:
        form = ServerInfoForm(instance=server_info)
    return render(request, 'asct/svinfo/update.html', {'form': form, 'server_info': server_info})

@login_required
def serverinfo_delete(request, pk):
    server_info = get_object_or_404(ServerInfo, id=pk)
    server_info.delete()
    return redirect('asct:serverinfo_list')

@login_required
def serverinfo_select(request):
    if request.method == 'POST':
        ssh_id = request.POST.get('ssh_id')
        if ssh_id:
            return serverinfo_run(request, ssh_id)

    # 현재 로그인한 사용자가 권한을 가진 서버만 조회
    sshinfos = SSHInfo.objects.filter(operators=request.user)
    
    return render(request, 'asct/svinfo/serverinfo_select.html', {'sshinfos': sshinfos})

@login_required
def serverinfo_run(request, ssh_id):
    ssh_info = get_object_or_404(SSHInfo, id=ssh_id)
    
    result = ""
    error = ""
    server_info_obj = None
    
    try:
        # 1. SSH 클라이언트 생성
        client = paramiko.SSHClient()
        # 2. 호스트 키 정책 설정 (알려지지 않은 호스트도 자동 허용 - 보안상 주의 필요)
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        # 3. 서버 접속
        client.connect(
            hostname=ssh_info.ip,
            port=ssh_info.port,
            username=ssh_info.login_id,
            password=ssh_info.password,
            timeout=10
        )
        
        # 4. 스크립트 업로드
        sftp = client.open_sftp()
        remote_script = f'/tmp/get_svinfo_{ssh_info.id}.sh' # type: ignore

        if request.method == 'POST' and request.FILES.get('script_file'):
            script_file = request.FILES['script_file']
            sftp.putfo(script_file, remote_script)
        else:
            script_path = os.path.join(settings.BASE_DIR, 'static', 'script_files', 'get_svinfo.sh')
            if os.path.exists(script_path):
                sftp.put(script_path, remote_script)
            else:
                raise FileNotFoundError("Default script file not found.")

        sftp.chmod(remote_script, 0o755)
        sftp.close()
        
        # 윈도우 개행문자 제거
        stdin, stdout, stderr = client.exec_command(f"sed -i 's/\r$//' {remote_script}")
        stdout.channel.recv_exit_status()
        # 수정된 remote_script 내용으로 실행
        stdin, stdout, stderr = client.exec_command(remote_script)
        exit_status = stdout.channel.recv_exit_status()
        
        output = stdout.read().decode('utf-8')
        err_output = stderr.read().decode('utf-8')
        
        # 원격 스크립트 삭제
        stdin, stdout, stderr = client.exec_command(f"rm {remote_script}")
        stdout.channel.recv_exit_status()
        
        client.close()
        
        if exit_status == 0:
            # JSON 파싱 (출력 중 JSON 부분만 추출)
            json_str = output[output.find('{'):output.rfind('}')+1]
            data = json.loads(json_str)
            
            # 6. 결과 저장 (ServerInfo 업데이트 또는 생성)
            server_info_obj, created = ServerInfo.objects.update_or_create(
                hostname=data['hostname'],
                defaults={
                    'sshinfos': ssh_info,
                    'ip1': data.get('ip1'),
                    'ip2': data.get('ip2'),
                    'os_version': data.get('os_version'),
                    'kernel_version': data.get('kernel_version'),
                    'cpu_cores': data.get('cpu_cores'),
                    'memory': data.get('memory'),
                    'total_disk': data.get('total_disk'),
                    'uptime': data.get('uptime'),
                    'data_time': data.get('data_time'),
                    'is_virtual': data.get('is_virtual'),
                    'cpu_usage': data.get('cpu_usage'),
                    'memory_usage': data.get('memory_usage'),
                    'disk_usage': data.get('disk_usage'),
                }
            )
            result = f"Successfully updated info for {data['hostname']}"
        else:
            error = f"Script execution failed:\n{err_output}"
            
    except Exception as e:
        error = f"Error: {str(e)}"

    # 결과를 보여줄 템플릿으로 렌더링 (result.html은 예시입니다)
    context = {
        'ssh_info': ssh_info,
        'result': result,
        'error': error,
        'server_info': server_info_obj,
    }
    return render(request, 'asct/svinfo/serverinfo_result.html', context)