from celery import shared_task
import paramiko
import json
import os
from django.conf import settings
from .models_basic import ServerInfo

@shared_task
def refresh_server_info_task(server_info_id):
    print('*'*30, server_info_id, '========== server_info_id ===============')
    try:
        server_info = ServerInfo.objects.get(id=server_info_id)
    except ServerInfo.DoesNotExist:
        return f"ServerInfo ID {server_info_id} not found."

    ssh_info = server_info.sshinfos
    if not ssh_info:
        return f"No SSH info for {server_info.hostname}"
    print('*'*30, ssh_info, '==== ssh_info ===============')

    # Default script path
    script_path = os.path.join(settings.BASE_DIR, 'static', 'script_files', 'get_svinfo.sh')
    if not os.path.exists(script_path):
        return "Default script file not found."
    print('*'*30, script_path, ' === script_path ================')

    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    print('*'*30, client, '====== client ===================')
    
    try:
        print('*'*30, 'before client connection ===================')
        client.connect(
            hostname=ssh_info.ip,
            port=ssh_info.port,
            username=ssh_info.login_id,
            password=ssh_info.password,
            timeout=10
        )
        print('*'*30, 'after client connection ===================')

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
