from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from .models_basic import Command, SSHInfo, CommandHistory, ServerInfo
from .forms_basic import CommandForm, SSHInfoForm, ServerInfoForm
from .run_by_ssh import run_ssh_cmd_serverinfo
from .views_common import common_export

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
    
    return render(request, 'asct/command/history_list.html', {'page_obj': page_obj})

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
            return redirect('asct:cmd_run', ssh_id=ssh_id, cmd_id=cmd_id)

    commands = Command.objects.all()
    # 현재 로그인한 사용자가 권한을 가진 서버만 조회
    sshinfos = SSHInfo.objects.filter(operators=request.user)
    
    return render(request, 'asct/command/select.html', {'commands': commands, 'sshinfos': sshinfos})

@login_required
def cmd_run(request, ssh_id, cmd_id):
    ssh_info = get_object_or_404(SSHInfo, id=ssh_id)
    command_obj = get_object_or_404(Command, id=cmd_id)
    
    result, error = run_ssh_cmd_serverinfo(request, ssh_info, command_obj)

    context = {
        'ssh_info': ssh_info,
        'command': command_obj,
        'result': result,
        'error': error,
    }
    return render(request, 'asct/command/result.html', context)

# =============== Paramiko server info 수집 ===============
@login_required
def serverinfo_list(request):
    serverinfos = ServerInfo.objects.all().order_by('hostname')
    
    paginator = Paginator(serverinfos, 15)
    page = request.GET.get("page")
    page_obj = paginator.get_page(page)
    
    return render(request, 'asct/svinfo/list.html', {'page_obj': page_obj})

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
def serverinfo_run(request, ssh_id): # create
    ssh_info = get_object_or_404(SSHInfo, id=ssh_id)
    
    server_info_obj, created, data, error = run_ssh_cmd_serverinfo(request, ssh_info )

    # 결과를 보여줄 템플릿으로 렌더링 (result.html은 예시입니다)
    context = {
        'ssh_info': ssh_info,
        'result': data,
        'error': error,
        'server_info': server_info_obj or created,
    }
    return render(request, 'asct/svinfo/serverinfo_result.html', context)

@login_required
def serverinfo_update(request, pk):
    server_info = get_object_or_404(ServerInfo, id=pk)
    if request.method == 'POST':
        if 'refresh_server' in request.POST:
            ssh_info = server_info.sshinfos
            server_info_obj, _, _, error = run_ssh_cmd_serverinfo(request, ssh_info )
            if error:
                messages.error(request, f"갱신 실패: {error}")
            else:
                messages.success(request, f"{server_info_obj.hostname} 갱신 성공") # type: ignore
            return redirect('asct:serverinfo_update', pk=pk)

        form = ServerInfoForm(request.POST, instance=server_info)
        if form.is_valid():
            form.save()
            return redirect('asct:serverinfo_list')
    else:
        form = ServerInfoForm(instance=server_info)
    return render(request, 'asct/svinfo/update.html', {'form': form, 'server_info': server_info})

@login_required
def serverinfo_export(request):
    headers = ['Hostname', 'IP1', 'IP2', 'OS Version', 'Kernel', 'CPU Cores', 'CPU(%)', 'Memory(GB)', 'Mem(%)', 'Disk(GB)', 'Disk(%)', 'Uptime(days)', 'Last Updated']
    
    def mapper(obj, dt_val):
        return [
            obj.hostname,
            obj.ip1,
            obj.ip2,
            obj.os_version_display,
            obj.kernel_version,
            obj.cpu_cores,
            obj.cpu_usage,
            obj.memory,
            obj.memory_usage,
            obj.total_disk,
            obj.disk_usage,
            obj.uptime,
            dt_val
        ]
        
    return common_export("server_info_list.xlsx", "Server Info", headers, ServerInfo, mapper)

# ws.append([ # type: ignore
#             server.hostname,
#             server.ip1,
#             server.ip2,
#             server.os_version_display,
#             server.kernel_version,
#             server.cpu_cores,
#             server.cpu_usage,
#             server.memory,
#             server.memory_usage,
#             server.total_disk,
#             server.disk_usage,
#             server.uptime,
#             data_time_val
#         ])