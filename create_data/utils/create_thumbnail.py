from events.models import Favorite
from django.db.models import Q

def generate_thumbnails():
    # 썸네일이 없거나(NULL) 빈 문자열인 항목 조회
    missing_thumbnails = Favorite.objects.filter(Q(thumbnail__isnull=True) | Q(thumbnail=''))
    
    total = missing_thumbnails.count()
    print(f"썸네일 생성 대상: 총 {total}건")
    
    success_count = 0
    for fav in missing_thumbnails:
        # 이미지가 존재하는 경우에만 처리
        if fav.image:
            try:
                print(f"[{success_count + 1}/{total}] 처리 중: {fav.name}")
                # save() 호출 시 모델 내부 로직에 의해 썸네일이 자동 생성됨
                fav.save()
                success_count += 1
            except Exception as e:
                print(f" -> 실패 ({fav.name}): {e}")
        else:
            print(f" -> 스킵 ({fav.name}): 원본 이미지 없음")
    print(f"\n작업 완료: {success_count}개의 썸네일이 생성되었습니다.")

# 함수 실행
generate_thumbnails()