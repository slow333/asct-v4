-- eshop_product 테이블에서 image가 NULL인 경우 기본값으로 설정
UPDATE eshop_product
SET image = 'products/no-image.jpg'
WHERE image IS NULL;

-- 확인: NULL인 image 개수 확인
SELECT COUNT(*) as null_image_count
FROM eshop_product
WHERE image IS NULL;

-- 확인: 업데이트된 행 개수 확인
SELECT COUNT(*) as total_records, 
       COUNT(CASE WHEN image = 'products/no-image.jpg' THEN 1 END) as default_image_count
FROM eshop_product;
