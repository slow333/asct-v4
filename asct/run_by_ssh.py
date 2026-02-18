from django.conf import settings
from .models_basic import CommandHistory, ServerInfo
from .models_resource import CPUUsage, MemoryUsage,NetworkUsage, DiskUsage
import paramiko, os, json, csv, io
from django.utils.timezone import make_aware
from datetime import datetime

def get_ssh_connection(ssh_obj):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(
        hostname=ssh_obj.ip,
        port=ssh_obj.port,
        username=ssh_obj.login_id,
        password=ssh_obj.password,
        timeout=10
    )
    return client

def common_sftp_result(request, client, ssh_obj, default_script_name, remote_script_prefix):
    sftp = client.open_sftp()
    remote_script = f'/tmp/{remote_script_prefix}_{ssh_obj.id}.sh'

    if request and request.method == 'POST' and request.FILES.get('script_file'):
        script_file = request.FILES['script_file']
        sftp.putfo(script_file, remote_script, confirm=False)
    else:
        script_path = os.path.join(settings.BASE_DIR, 'asct', 'script_files', default_script_name)
        if os.path.exists(script_path):
            sftp.put(script_path, remote_script, confirm=False)
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
        return None, f"Script execution failed: {error_msg}", None
    
    return output, error_msg, remote_script

def common_ssh_usage_collector(request, ssh_obj, default_script_name, remote_script_prefix, row_processor):
    # error_msg = ""
    try:
        client = get_ssh_connection(ssh_obj)
        # 4. 명령어 실행
        output, script_error, remote_script = common_sftp_result(request, client, ssh_obj, default_script_name, remote_script_prefix) # type: ignore
        
        if output is None:
            return None, False, {}, script_error
        csv_file_path = ""
        for line in output.splitlines(): # type: ignore
            if "Successfully generated CSV:" in line:
                parts = line.split(": ")
                if len(parts) > 1:
                    csv_file_path = parts[1].strip()
        if not csv_file_path:
            client.exec_command(f"rm {remote_script}")
            client.close()
            return None, False, {}, "CSV file path not found in script output."

        # Read CSV content
        stdin, stdout, stderr = client.exec_command(f"cat {csv_file_path}")
        csv_content = stdout.read().decode('utf-8')
        cat_error = stderr.read().decode('utf-8')
        
        # Cleanup remote files
        client.exec_command(f"rm {remote_script} {csv_file_path}")
        client.close()

        if cat_error:
            return None, False, {}, f"Failed to read CSV: {cat_error}. Script stderr: {script_error}"

        # Parse CSV and Save to DB
        f = io.StringIO(csv_content)
        saved_count = 0
        try:
            reader = csv.DictReader(f)
            if not reader.fieldnames:
                return None, False, {}, f"CSV header is missing or empty. Script stderr: {script_error}"

            for row in reader:
                try:
                    aware_dt = None
                    if row.get('Date'):
                        date_str = row['Date'].strip().replace('"', '').replace("'", "").replace('T', ' ')[:19]
                        dt_obj = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
                        aware_dt = make_aware(dt_obj)
                    
                    if row_processor(row, ssh_obj, aware_dt):
                        saved_count += 1
                except ValueError as e:
                    print(f"Date parse error: {e}")
                    continue
                except Exception as e:
                    print(f"Row processing error: {e}")
                    continue
        except csv.Error as e:
            return None, False, {}, f"CSV parsing error: {str(e)}"

        return None, False, {'count': saved_count}, script_error
        
    except Exception as e:
        return None, False, {}, f"## 연결실패: {str(e)} ##"

# ========= 파일이용 disk usage 수집 ==========
def run_ssh_disk_usage(request, ssh_obj):
    
    client = get_ssh_connection(ssh_obj)
    output, error_msg, remote_script = common_sftp_result(request, client, ssh_obj, 'get_disk_usage_df.sh', "get_disk_usage_df_") # type: ignore

    if output is None:
        return None, False, {}, error_msg
    client.close()
    
    # 6. JSON 파싱 (출력 중 JSON 부분만 추출)
    json_str = output[output.find('{'):output.rfind('}')+1] # type: ignore
    data = json.loads(json_str)
    
    # 결과 저장 (ServerInfo 업데이트 또는 생성)
    total_val = data.get('local_total', 0)
    disk_usage_val = data.get('local_usage_p', 0.0)

    disk_usage_obj, created = DiskUsage.objects.update_or_create(
        hostname=data['hostname'],
        ip=data['ip_addr'],
        checked_at=datetime.now(),
        storage_type=data['storage_type'],
        defaults={
            'ssh_info': ssh_obj,
            'local_total': int(total_val) if total_val else 0,
            'local_usage_p': int(disk_usage_val) if disk_usage_val else 0,
            'is_confirmed': True
        }
    )
    return disk_usage_obj, created, data, error_msg

# ========= Paramiko 실행:  파일이용 traffic usage 수집 ==========
def run_ssh_traffic_usage(request, ssh_obj):
    def processor(row, ssh_obj, aware_dt):
        rx_val = row.get('rxkB/s', '').strip()
        tx_val = row.get('txkB/s', '').strip()
        if len(row['IFACE']) > 20:
            return False

        NetworkUsage.objects.update_or_create(
            hostname=row['hostname'].strip(),
            ip=row['IP'].strip(),
            data_time=aware_dt,
            if_name=row['IFACE'].strip(),
            speed=row['Speed'].strip(),
            defaults={
                'ssh_info': ssh_obj,
                'rxkB_s': float(rx_val) if rx_val else 0.0,
                'txkB_s': float(tx_val) if tx_val else 0.0,
                'is_confirmed': True
            }
        )
        return True

    return common_ssh_usage_collector(request, ssh_obj, 'get_month_traffic_usage.sh', 'month_traffic_usage', processor)

# ========= 파일이용 cpu usage 수집 ==========
def run_ssh_cpu_usage(request, ssh_obj):
    
    def processor(row, ssh_obj, aware_dt):
        CPUUsage.objects.update_or_create(
            hostname=row['hostname'].strip(),
            ip=row['IP'].strip(),
            data_time=aware_dt,
            defaults={
                'ssh_info': ssh_obj,
                'cpu_cores': int(row['Cpu_cores']) if row.get('Cpu_cores') else 1,
                'usage_p': float(row['Total_Usage(%)']),
                'is_confirmed': True
            }
        )
        return True

    return common_ssh_usage_collector(request, ssh_obj, 'get_month_cpu_usage.sh', 'month_cpu_usage', processor)

# ========= 파일이용 memory usage 수집 ==========
def run_ssh_memory_usage(request, ssh_obj):
    # hostname,IP,Date,Total_Mem,Usage(%)
    def processor(row, ssh_obj, aware_dt):
        MemoryUsage.objects.update_or_create(
            hostname=row['hostname'].strip(),
            ip=row['IP'].strip(),
            data_time=aware_dt,
            defaults={
                'ssh_info': ssh_obj,
                'total_memory': int(row['Total_Mem']) if row.get('Total_Mem') else 0,
                'usage_p': float(row['Usage(%)']),
                'is_confirmed': True
            }
        )
        return True

    return common_ssh_usage_collector(request, ssh_obj, 'get_month_memory_usage.sh', 'month_memory_usage', processor)

# ========= Paramiko 실행 command이용 수집, 파일이용 server info 수집 ==========
def run_ssh_cmd_serverinfo(request, ssh_obj, cmd_obj=None):
    result = ""
    error = ""
    server_info_obj=None

    try:
        # 1. SSH 클라이언트 생성
        client = get_ssh_connection(ssh_obj)

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
            output, error_msg, remote_script = common_sftp_result(request, client, ssh_obj, 'get_svinfo.sh', "get_svinfo_") # type: ignore
            
            if output is None:
                return None, False, {}, error_msg
            client.close()
            
            # 6. JSON 파싱 (출력 중 JSON 부분만 추출)
            json_str = output[output.find('{'):output.rfind('}')+1] # type: ignore
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
            return server_info_obj, created, data, error_msg
        
    except Exception as e:
        if cmd_obj:
            return "", f"## 연결실패: {str(e)} ##"
        else:
            return None, False, {}, f"## 연결실패: {str(e)} ##"
