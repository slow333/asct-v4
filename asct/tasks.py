from celery import shared_task
import paramiko, json, os
from django.conf import settings
from .run_by_ssh import get_ssh_connection
import logging

logger = logging.getLogger(__name__)

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
    script_path = os.path.join(settings.BASE_DIR, 'static', 'script_files', 'get_svinfo.sh')
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
        sftp.put(script_path, remote_script)
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
