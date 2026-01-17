import os
import sys
import django

# 프로젝트 루트 디렉토리를 sys.path에 추가 (config.settings를 찾기 위함)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from django.contrib.auth.hashers import make_password

if __name__ == "__main__":
    # 커맨드라인 인자로 비밀번호를 입력받거나, 없으면 '1111' 사용
    raw_password = sys.argv[1] if len(sys.argv) > 1 else "1111"
    hashed_password = make_password(raw_password)
    
    print(f"Raw Password: {raw_password}")
    print(f"Encoded Password: {hashed_password}")
