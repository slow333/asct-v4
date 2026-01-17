# 1. 필요한 모듈을 가져옵니다.
from idols.models import Idol
from django.core.files import File
import os

# 2. 등록할 이미지 파일의 경로를 지정합니다.
#    'B:\coding\images\idol' 
#    Windows 경로의 경우 역슬래시(\)를 두 번 쓰거나(B:\\coding\\...) 경로 문자열 앞에 r을 붙여야 합니다(r'B:\coding\...').
image_folder_path = r'B:\images\idol'
next_id = 1
# 3. 폴더가 존재하는지 확인합니다.
if not os.path.isdir(image_folder_path):
    print(f"오류: '{image_folder_path}' 폴더가 존재하지 않습니다.")
else:
    # 4. 폴더 내의 모든 파일과 하위 폴더를 순회합니다.
    for dirpath, _, filenames in os.walk(image_folder_path):
        for filename in filenames:
            # 5. 이미지 파일 확장자인지 확인합니다.
            if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp', '.webp', '.heic')):
                file_path = os.path.join(dirpath, filename)
    
                # 6. 이미지 파일을 엽니다.
                with open(file_path, 'rb') as f:
                    # 7. Django의 File 객체로 만듭니다.
                    image_file = File(f, name=filename)
    
                    # 8. 파일명을 title로 사용합니다 (확장자 제외).
                    title = os.path.splitext(filename)[0]
    
                    # 9. Idol 객체를 생성하고 저장합니다.
                    created = Idol(
                        id=next_id,
                        title=title,
                        image=image_file
                    )
                    created.save()
                    next_id += 1
                    if created:
                        print(f"성공: '{filename}' 이미지를 등록했습니다.")

# python manage.py shell
# exec(open('create_data/regist_images.py', encoding='utf-8').read())
