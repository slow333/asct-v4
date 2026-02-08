import csv
import os
from datetime import datetime
from django.conf import settings
from django.utils.timezone import make_aware

# 모델 import (monitor 앱의 NetworkUsage 모델이 있다고 가정)
# 앱 이름이 다르다면 'monitor' 부분을 실제 앱 이름으로 변경하세요.
try:
    from monitor.models import NetworkUsage
except ImportError:
    print("오류: 'monitor' 앱 또는 'NetworkUsage' 모델을 찾을 수 없습니다.")
    print("먼저 models.py에 NetworkUsage 모델을 정의해주세요.")
    # 모델을 찾을 수 없으면 스크립트 실행을 중단하지 않고, 정의된 곳을 찾도록 유도하거나 주석 처리 후 진행

# CSV 파일 경로 설정
# traffic_monitor.sh에서 생성한 파일 경로 (/tmp/traffic_stats.csv)
CSV_FILE_PATH = r'/tmp/traffic_stats.csv'

# Windows 개발 환경에서 실행 시 경로 보정 (필요 시 수정)
if os.name == 'nt':
    # 예: C:\tmp\traffic_stats.csv 또는 프로젝트 루트의 tmp 폴더 등
    # 파일을 Windows 경로로 복사해 두어야 합니다.
    CSV_FILE_PATH = r'C:\tmp\traffic_stats.csv'

def parse_timestamp(ts_str):
    """타임스탬프 문자열을 datetime 객체로 변환"""
    try:
        # 1. Epoch timestamp (숫자만 있는 경우)
        if ts_str.isdigit():
            return datetime.fromtimestamp(int(ts_str))
        
        # 2. 표준 날짜 포맷 (YYYY-MM-DD HH:MM:SS)
        # sadf 버전에 따라 포맷이 다를 수 있으므로 확인 필요
        return datetime.strptime(ts_str, "%Y-%m-%d %H:%M:%S")
    except ValueError:
        return None

def import_data():
    if not os.path.exists(CSV_FILE_PATH):
        print(f"파일을 찾을 수 없습니다: {CSV_FILE_PATH}")
        print("traffic_monitor.sh를 실행하여 CSV 파일을 생성하거나, 파일 경로를 확인하세요.")
        return

    print(f"데이터 가져오기 시작: {CSV_FILE_PATH}")
    
    with open(CSV_FILE_PATH, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        
        created_count = 0
        skipped_count = 0
        
        for row in reader:
            # CSV 헤더: hostname,timestamp,IFACE,rxkB/s,txkB/s
            hostname = row.get('hostname')
            ts_str = row.get('timestamp')
            iface = row.get('IFACE')
            rx_kbs_str = row.get('rxkB/s')
            tx_kbs_str = row.get('txkB/s')

            if not (hostname and ts_str and iface):
                continue

            # Timestamp 파싱 및 Timezone 처리
            dt = parse_timestamp(ts_str)
            if dt is None:
                continue
            
            if settings.USE_TZ:
                dt = make_aware(dt)

            # 중복 데이터 확인 후 저장 (get_or_create 사용 가능하지만, 여기서는 명시적 확인)
            if not NetworkUsage.objects.filter(hostname=hostname, timestamp=dt, interface=iface).exists():
                NetworkUsage.objects.create(
                    hostname=hostname,
                    timestamp=dt,
                    interface=iface,
                    rx_kbs=float(rx_kbs_str),
                    tx_kbs=float(tx_kbs_str)
                )
                created_count += 1
            else:
                skipped_count += 1

    print(f"작업 완료: {created_count}건 저장됨, {skipped_count}건 중복 생략됨.")

# 실행
import_data()
