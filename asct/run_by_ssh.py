from django.conf import settings
from .models_basic import CommandHistory, ServerInfo
from .models_resource import CPUUsage, MemoryUsage
from .forms_resource import CPUUsageForm
import paramiko, os, json, csv, io
from django.utils.timezone import make_aware
from datetime import datetime

# ========= Paramiko 실행:  파일이용 cpu usage 수집 ==========
def run_ssh_cpu_usage(request, ssh_obj):
    error_msg = ""

    try:
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(
            hostname=ssh_obj.ip,
            port=ssh_obj.port,
            username=ssh_obj.login_id,
            password=ssh_obj.password,
            timeout=10
        )
        # 4. 명령어 실행
        sftp = client.open_sftp()
        remote_script = f'/tmp/month_cpu_usage_{ssh_obj.id}.sh' # type: ignore

        if request.method == 'POST' and request.FILES.get('script_file'):
            script_file = request.FILES['script_file']
            sftp.putfo(script_file, remote_script)
        else:
            script_path = os.path.join(settings.BASE_DIR, 'static', 'script_files', 'get_month_cpu_usage.sh')
            if os.path.exists(script_path):
                sftp.put(script_path, remote_script)
            else:
                raise FileNotFoundError("Default script file not found.")
        
        sftp.chmod(remote_script, 0o755)
        sftp.close()
        # 3. Execute Script (Fix windows line endings first)
        client.exec_command(f"sed -i 's/\r$//' {remote_script}")
        
        stdin, stdout, stderr = client.exec_command(remote_script)
        exit_status = stdout.channel.recv_exit_status()
        
        output = stdout.read().decode('utf-8')
        error_msg = stderr.read().decode('utf-8')

        if exit_status != 0:
            client.exec_command(f"rm {remote_script}")
            client.close()
            return None, False, {}, f"Script execution failed: {error_msg}"

        # Parse output to find CSV filename
        csv_file_path = ""
        for line in output.splitlines():
            if "Successfully generated CSV:" in line:
                csv_file_path = line.split(": ")[1].strip()
        
        if not csv_file_path:
            client.exec_command(f"rm {remote_script}")
            client.close()
            return None, False, {}, "CSV file path not found in script output."

        # Read CSV content
        stdin, stdout, stderr = client.exec_command(f"cat {csv_file_path}")
        csv_content = stdout.read().decode('utf-8')
        
        # Cleanup remote files
        client.exec_command(f"rm {remote_script} {csv_file_path}")
        client.close()

        # Parse CSV and Save to DB
        f = io.StringIO(csv_content)
        reader = csv.DictReader(f)
        
        saved_count = 0
        for row in reader:
            # CSV Headers: Hostname,IP,Date,Cpu_cores,Total_Usage(%)
            
            try:
                # Make datetime aware to avoid RuntimeWarning
                # Handle RHEL 10 / Modern sysstat formats (ISO 8601 with T, quotes)
                # Replace T with space and take first 19 chars to ignore timezone/garbage
                date_str = row['Date'].strip().replace('"', '').replace("'", "").replace('T', ' ')[:19]
                dt_obj = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
                aware_dt = make_aware(dt_obj)
                
                CPUUsage.objects.update_or_create(
                    hostname=row['Hostname'].strip(),
                    ip=row['IP'].strip(),
                    data_time=aware_dt,
                    defaults={
                        'ssh_info': ssh_obj,
                        'cpu_cores': int(row['Cpu_cores']) if row.get('Cpu_cores') else 1,
                        'usage_p': float(row['Total_Usage(%)']),
                        'is_confirmed': True
                    }
                )
                saved_count += 1
            except ValueError as e:
                print(f"Date parse error for {row.get('Hostname')}: {row.get('Date')} - {e}")
                continue
            
        return None, False, {'count': saved_count}, error_msg
        
    except Exception as e:
        return None, False, {}, f"## 연결실패: {str(e)} ##"

# ========= Paramiko 실행:  파일이용 memory usage 수집 ==========
def run_ssh_memory_usage(request, ssh_obj):
    error_msg = ""

    try:
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(
            hostname=ssh_obj.ip,
            port=ssh_obj.port,
            username=ssh_obj.login_id,
            password=ssh_obj.password,
            timeout=10
        )
        
        sftp = client.open_sftp()
        remote_script = f'/tmp/month_memory_usage_{ssh_obj.id}.sh'

        script_path = os.path.join(settings.BASE_DIR, 'static', 'script_files', 'get_month_memory_usage.sh')
        if os.path.exists(script_path):
            sftp.put(script_path, remote_script)
        else:
            raise FileNotFoundError("Default script file not found.")
        
        sftp.chmod(remote_script, 0o755)
        sftp.close()
        
        client.exec_command(f"sed -i 's/\r$//' {remote_script}")
        
        stdin, stdout, stderr = client.exec_command(remote_script)
        exit_status = stdout.channel.recv_exit_status()
        
        output = stdout.read().decode('utf-8')
        error_msg = stderr.read().decode('utf-8')

        if exit_status != 0:
            client.exec_command(f"rm {remote_script}")
            client.close()
            return None, False, {}, f"Script execution failed: {error_msg}"

        csv_file_path = ""
        for line in output.splitlines():
            if "Successfully generated CSV:" in line:
                csv_file_path = line.split(": ")[1].strip()
        
        if not csv_file_path:
            client.exec_command(f"rm {remote_script}")
            client.close()
            return None, False, {}, "CSV file path not found in script output."

        stdin, stdout, stderr = client.exec_command(f"cat {csv_file_path}")
        csv_content = stdout.read().decode('utf-8')
        
        client.exec_command(f"rm {remote_script} {csv_file_path}")
        client.close()

        f = io.StringIO(csv_content)
        reader = csv.DictReader(f)
        
        saved_count = 0
        for row in reader:
            try:
                date_str = row['Date'].strip().replace('"', '').replace("'", "").replace('T', ' ')[:19]
                dt_obj = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
                aware_dt = make_aware(dt_obj)
                
                MemoryUsage.objects.update_or_create(
                    hostname=row['Hostname'].strip(),
                    ip=row['IP'].strip(),
                    data_time=aware_dt,
                    defaults={
                        'ssh_info': ssh_obj,
                        'total_memory': int(row['Total_Mem']) if row.get('Total_Mem') else 0,
                        'usage_p': float(row['Usage(%)']),
                        'is_confirmed': True
                    }
                )
                saved_count += 1
            except ValueError:
                continue
            
        return None, False, {'count': saved_count}, error_msg
        
    except Exception as e:
        return None, False, {}, f"## 연결실패: {str(e)} ##"

# ========= Paramiko 실행 command이용 수집, 파일이용 server info 수집 ==========
def run_ssh_cmd_serverinfo(request, ssh_obj, cmd_obj=None):
    result = ""
    error = ""
    server_info_obj=None

    try:
        # 1. SSH 클라이언트 생성
        client = paramiko.SSHClient()
        # 2. 호스트 키 정책 설정 (알려지지 않은 호스트도 자동 허용 - 보안상 주의 필요)
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        # 3. 서버 접속
        client.connect(
            hostname=ssh_obj.ip,
            port=ssh_obj.port,
            username=ssh_obj.login_id,
            password=ssh_obj.password,
            timeout=10
        )

        # 4. 명령어 실행
        if cmd_obj:
            stdin, stdout, stderr = client.exec_command(cmd_obj.script) # type: ignore
            result = stdout.read().decode('utf-8')
            error = stderr.read().decode('utf-8')
            client.close()
            
            CommandHistory.objects.create(
                ssh_info=ssh_obj,
                command=cmd_obj,
                executed_by=request.user,
                stdout=result,
                stderr=error
            )
            return result, error
            
        else:
            sftp = client.open_sftp()
            remote_script = f'/tmp/get_svinfo_{ssh_obj.id}.sh' # type: ignore

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
            sftp.close()# 3. Execute Script (Fix windows line endings first)
            
            client.exec_command(f"sed -i 's/\r$//' {remote_script}")
            
            stdin, stdout, stderr = client.exec_command(remote_script)
            exit_status = stdout.channel.recv_exit_status()
            
            # 4. Cleanup
            client.exec_command(f"rm {remote_script}")
            
            # 5. 결과 읽기 (bytes를 utf-8로 디코딩)
            result = stdout.read().decode('utf-8')
            error = stderr.read().decode('utf-8')
            client.close()
            
            # 6. JSON 파싱 (출력 중 JSON 부분만 추출)
            json_str = result[result.find('{'):result.rfind('}')+1]
            data = json.loads(json_str)
            
            # 결과 저장 (ServerInfo 업데이트 또는 생성)
            server_info_obj, created = ServerInfo.objects.update_or_create(
                hostname=data['hostname'],
                defaults={
                    'sshinfos': ssh_obj,
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
            return server_info_obj, created, data, error
        
    except Exception as e:
        return ("", f"## 연결실패: {str(e)} ##")
