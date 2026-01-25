import os
import sys
import django

# 프로젝트 루트 디렉토리를 sys.path에 추가
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from django.core.management.color import no_style
from django.db import connection, connections
from django.apps import apps

def fix_sequences(app_name):
    """
    지정된 앱의 모델들에 대한 시퀀스(Auto Increment ID)를 현재 데이터의 최대값에 맞춰 재설정합니다.
    """
    try:
        app_config = apps.get_app_config(app_name)
    except LookupError:
        print(f"App '{app_name}'을(를) 찾을 수 없습니다.")
        return

    models = app_config.get_models()
    # 시퀀스 리셋 SQL 구문 생성 (PostgreSQL 등에서 유효)
    sequence_sql = connections['default'].ops.sequence_reset_sql(no_style(), models)
    
    if sequence_sql:
        print(f"--- '{app_name}' 앱의 시퀀스 재설정 시작 ---")
        with connection.cursor() as cursor:
            for sql in sequence_sql:
                cursor.execute(sql)
        print("--- 완료 ---")
    else:
        print(f"'{app_name}' 앱에 재설정할 시퀀스가 없습니다.")

if __name__ == "__main__":
    # 인자로 앱 이름을 받거나, 기본값으로 'idols' 사용
    target_app = sys.argv[1] if len(sys.argv) > 1 else 'idols'
    fix_sequences(target_app)
