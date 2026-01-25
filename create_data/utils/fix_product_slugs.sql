-- 한글 또는 특수문자가 포함된 product name을 ASCII slug로 변환하는 스크립트
-- slugify 방식: 소문자로 변환, 공백과 특수문자를 하이픈으로 변환, 한글은 제거 후 name 기반의 숫자 ID 사용

-- 1단계: 한글/특수문자만 있는 상품들에 대해 기본 슬러그 생성 (id 기반)
UPDATE eshop_product 
SET slug = LOWER(CONCAT('product-', id))
WHERE id IN (
    SELECT id FROM eshop_product 
    WHERE name ~ '[^a-zA-Z0-9\s\-]' -- 한글, 한자, 특수문자 포함 확인
);

-- 2단계: 영문 이름이 있는 상품들은 이름 기반 slug 생성
UPDATE eshop_product 
SET slug = LOWER(REGEXP_REPLACE(name, '\s+', '-', 'g'))
WHERE name ~ '^[a-zA-Z0-9\s\-]+$' -- 영문, 숫자, 공백, 하이픈만 포함
AND slug != name;

-- 확인
SELECT id, name, slug FROM eshop_product ORDER BY id;
