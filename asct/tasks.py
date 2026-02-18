from celery import shared_task # type: ignore
import paramiko, json, os
from datetime import timedelta
from django.utils import timezone
from django.conf import settings
from .run_by_ssh import get_ssh_connection, run_ssh_cpu_usage, run_ssh_memory_usage, run_ssh_traffic_usage
import logging

logger = logging.getLogger(__name__)

@shared_task
def schedule_server_info_collection():
    # 작업을 실행할 때 모델을 임포트하여 앱 레지스트리 문제를 방지합니다.
    from .models_basic import SSHInfo
    
    # 모든 SSHInfo에 대해 개별적으로 Task 실행
    for ssh_info in SSHInfo.objects.all():
        collect_server_info_task.delay(ssh_info.id) # type: ignore

@shared_task
def collect_server_info_task(ssh_id):
    from .models_basic import SSHInfo, ServerInfo

    try:
        ssh_info = SSHInfo.objects.get(id=ssh_id)
    except SSHInfo.DoesNotExist:
        return f"SSHInfo ID {ssh_id} not found."

    # 스크립트 경로 설정 (run_by_ssh.py와 동일한 경로 사용)
    script_path = os.path.join(settings.BASE_DIR, 'asct', 'script_files', 'get_svinfo.sh')
    if not os.path.exists(script_path):
        return f"Script file not found: {script_path}"

    try:
        client = get_ssh_connection(ssh_info)
        
        # SFTP로 스크립트 전송
        sftp = client.open_sftp()
        remote_script = f'/tmp/get_svinfo_{ssh_info.id}.sh' # type: ignore
        sftp.put(script_path, remote_script, confirm=False)
        sftp.chmod(remote_script, 0o755)
        sftp.close()

        # 윈도우 개행문자 제거 및 실행
        client.exec_command(f"sed -i 's/\r$//' {remote_script}")
        stdin, stdout, stderr = client.exec_command(remote_script)
        exit_status = stdout.channel.recv_exit_status()
        output = stdout.read().decode('utf-8')
        
        # 원격 스크립트 삭제
        client.exec_command(f"rm {remote_script}")
        client.close()

        if exit_status == 0:
            # JSON 파싱
            json_str = output[output.find('{'):output.rfind('}')+1]
            data = json.loads(json_str)
            
            # ServerInfo 생성 또는 업데이트
            ServerInfo.objects.update_or_create(
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
            return f"Successfully collected info for {data['hostname']}"
        else:
            error_msg = stderr.read().decode('utf-8')
            return f"Script execution failed for {ssh_info.ip}: {error_msg}"

    except Exception as e:
        logger.error(f"Error collecting server info for {ssh_info.ip}: {e}")
        return f"Error: {str(e)}"

@shared_task
def schedule_disk_usage_collection():
    # 작업을 실행할 때 모델을 임포트하여 앱 레지스트리 문제를 방지합니다.
    from .models_basic import SSHInfo
    
    ssh_infos = SSHInfo.objects.all()
    server_list = [
        (info.ip, info.login_id, info.password, info.port) for info in ssh_infos
    ]
    if server_list:
        collect_disk_usage.delay(server_list)

@shared_task
def collect_disk_usage(server_list):
    from .models_basic import SSHInfo
    from .models_resource import DiskUsage

    for ssh_info in server_list:
        try:
            ip, username, password, port = ssh_info
            
            ssh_obj = SSHInfo.objects.filter(ip=ip).first()
            if not ssh_obj:
                continue
            ssh = get_ssh_connection(ssh_obj)

            stdin, hostname, stderr = ssh.exec_command("hostname")
            hostname = hostname.read().decode().strip()

            stdin, ip_list, stderr = ssh.exec_command("hostname -I")
            ip_list = ip_list.read().decode().strip().split()
            ip_address = ip_list[0] if ip_list else ip

            stdin, disk_usage, stderr = ssh.exec_command("df -h")
            lines = disk_usage.read().decode().strip().split("\n")[1:]  # 헤더 제외

            for line in lines:
                parts = line.split()
                if len(parts) < 6:
                    continue
                device, mount, use_p, size_str = parts[0], parts[5], parts[4], parts[1]
                use_p = int(use_p.strip("%"))
                if device.strip() in ['tmpfs', 'devtmpfs', 'overlay'] or device.startswith('/dev/loop'):
                    continue
                size = 0
                if size_str.endswith('G'):
                    size = int(float(size_str.strip('G')))
                elif size_str.endswith('M'):
                    size = int(float(size_str.strip('M')) / 1024)
                elif size_str.endswith('T'):
                    size = int(float(size_str.strip('T')) * 1024)

                DiskUsage.objects.create(
                    ssh_info=ssh_obj,
                    hostname=hostname,
                    ip=ip_address,
                    device=device,
                    mounted=mount,
                    size=size,
                    use_p=use_p,
                )

            ssh.close()
        except Exception as e:
            logger.error(f"Error collecting disk usage for {ip}: {e}")

@shared_task
def refresh_server_info_task(server_info_id):
    from .models_basic import ServerInfo

    try:
        server_info = ServerInfo.objects.get(id=server_info_id)
    except ServerInfo.DoesNotExist:
        return f"ServerInfo ID {server_info_id} not found."

    ssh_info = server_info.sshinfos
    if not ssh_info:
        return f"No SSH info for {server_info.hostname}"

    # Default script path
    script_path = os.path.join(settings.BASE_DIR, 'asct', 'script_files', 'get_svinfo.sh')
    if not os.path.exists(script_path):
        return "Default script file not found."

    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        client.connect(
            hostname=ssh_info.ip,
            port=ssh_info.port,
            username=ssh_info.login_id,
            password=ssh_info.password,
            timeout=10
        )

        sftp = client.open_sftp()
        remote_script = f'/tmp/get_svinfo_{ssh_info.id}.sh' # type: ignore
        sftp.put(script_path, remote_script, confirm=False)
        sftp.chmod(remote_script, 0o755)
        sftp.close()

        # 윈도우 개행문자 제거
        stdin, stdout, stderr = client.exec_command(f"sed -i 's/\r$//' {remote_script}")
        stdout.channel.recv_exit_status()

        stdin, stdout, stderr = client.exec_command(remote_script)
        exit_status = stdout.channel.recv_exit_status()
        output = stdout.read().decode('utf-8')
        
        # 원격 스크립트 삭제
        stdin, stdout, stderr = client.exec_command(f"rm {remote_script}")
        stdout.channel.recv_exit_status()
        
        if exit_status == 0:
            # Extract JSON
            json_str = output[output.find('{'):output.rfind('}')+1]
            data = json.loads(json_str)
            
            # Update fields
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
            return f"Successfully updated {server_info.hostname}"
        else:
            return f"Script execution failed for {server_info.hostname}"
    except Exception as e:
        return f"Connection failed for {server_info.hostname} ({ssh_info.ip}:{ssh_info.port}): {e}"
    finally:
        client.close()

# Metric 수집 핸들러 매핑
METRIC_HANDLERS = {
    'cpu': run_ssh_cpu_usage,
    'memory': run_ssh_memory_usage,
    'traffic': run_ssh_traffic_usage,
}

@shared_task
def collect_metric_task(ssh_id, metric_type):
    from .models_basic import SSHInfo
    
    handler = METRIC_HANDLERS.get(metric_type)
    if not handler:
        return f"Unknown metric type: {metric_type}"

    try:
        ssh_info = SSHInfo.objects.get(id=ssh_id)
        # run_ssh_* 함수들은 (request, ssh_obj) 인자를 받음. request는 None으로 전달.
        _, _, data, error = handler(None, ssh_info)
        
        if error:
            logger.error(f"Error collecting {metric_type} usage for {ssh_info}: {error}")
            return f"Error collecting {metric_type} usage for {ssh_info}: {error}"
        return f"Successfully collected {metric_type} usage for {ssh_info}: {data}"
    except Exception as e:
        logger.error(f"Exception for {ssh_id} ({metric_type}): {e}", exc_info=True)
        return f"Exception for {ssh_id} ({metric_type}): {e}"

@shared_task
def schedule_cpu_usage_collection():
    from .models_basic import SSHInfo
    for ssh_info in SSHInfo.objects.all():
        collect_metric_task.delay(ssh_info.id, 'cpu') # type: ignore

@shared_task
def schedule_memory_usage_collection():
    from .models_basic import SSHInfo
    logger.info("########### run tasks: memory usage collection started =========")
    for ssh_info in SSHInfo.objects.all():
        collect_metric_task.delay(ssh_info.id, 'memory') # type: ignore

@shared_task
def schedule_traffic_usage_collection():
    from .models_basic import SSHInfo
    for ssh_info in SSHInfo.objects.all():
        collect_metric_task.delay(ssh_info.id, 'traffic') # type: ignore

@shared_task
def cleanup_old_data(days=30):
    """
    지정된 기간(일)보다 오래된 리소스 사용량 데이터를 삭제합니다.
    """
    from .models_resource import CPUUsage, MemoryUsage, NetworkUsage, DiskUsage
    
    threshold = timezone.now() - timedelta(days=days)
    
    # data_time 필드를 사용하는 모델들
    cpu_cnt, _ = CPUUsage.objects.filter(data_time__lt=threshold).delete()
    mem_cnt, _ = MemoryUsage.objects.filter(data_time__lt=threshold).delete()
    net_cnt, _ = NetworkUsage.objects.filter(data_time__lt=threshold).delete()
    
    # checked_at 필드를 사용하는 모델
    disk_cnt, _ = DiskUsage.objects.filter(checked_at__lt=threshold).delete()
    
    return f"Cleanup completed (older than {days} days): CPU({cpu_cnt}), Mem({mem_cnt}), Traffic({net_cnt}), Disk({disk_cnt})"
