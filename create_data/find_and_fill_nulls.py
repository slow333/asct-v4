#!/usr/bin/env python
"""
PostgreSQL에서 null 값을 찾아서 채우는 스크립트
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.db import connection
from django.apps import apps

def find_null_values():
    """모든 테이블에서 null 값을 찾습니다"""
    
    print("=" * 80)
    print("PostgreSQL 데이터베이스에서 NULL 값 찾기")
    print("=" * 80)
    
    with connection.cursor() as cursor:
        # 모든 테이블 조회
        cursor.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public' 
            AND table_type = 'BASE TABLE'
            ORDER BY table_name
        """)
        
        tables = cursor.fetchall()
        
        null_summary = {}
        
        for (table_name,) in tables:
            # 각 테이블의 컬럼 조회
            cursor.execute(f"""
                SELECT column_name, data_type, is_nullable
                FROM information_schema.columns
                WHERE table_name = '{table_name}'
                ORDER BY column_name
            """)
            
            columns = cursor.fetchall()
            
            for column_name, data_type, is_nullable in columns:
                if is_nullable == 'YES':
                    # NULL 값의 개수 확인
                    cursor.execute(f"""
                        SELECT COUNT(*) 
                        FROM "{table_name}" 
                        WHERE "{column_name}" IS NULL
                    """)
                    
                    null_count = cursor.fetchone()[0]
                    
                    if null_count > 0:
                        key = f"{table_name}.{column_name}"
                        
                        # 전체 행 개수도 확인
                        cursor.execute(f'SELECT COUNT(*) FROM "{table_name}"')
                        total_count = cursor.fetchone()[0]
                        
                        null_summary[key] = {
                            'null_count': null_count,
                            'total_count': total_count,
                            'percentage': (null_count / total_count * 100) if total_count > 0 else 0,
                            'data_type': data_type
                        }
        
        if null_summary:
            print(f"\n발견된 NULL 값: {len(null_summary)}개\n")
            for table_col, info in sorted(null_summary.items()):
                print(f"📊 {table_col}")
                print(f"   - 타입: {info['data_type']}")
                print(f"   - NULL 개수: {info['null_count']}/{info['total_count']} ({info['percentage']:.1f}%)")
                print()
        else:
            print("\n✅ NULL 값이 없습니다!")
        
        return null_summary

def fill_null_values_interactive(null_summary):
    """대화형으로 NULL 값을 채웁니다"""
    
    if not null_summary:
        print("채울 NULL 값이 없습니다.")
        return
    
    print("\n" + "=" * 80)
    print("NULL 값 채우기")
    print("=" * 80)
    
    for idx, (table_col, info) in enumerate(sorted(null_summary.items()), 1):
        table_name, column_name = table_col.split('.')
        
        print(f"\n[{idx}] {table_col} (타입: {info['data_type']}, NULL 개수: {info['null_count']})")
        print("옵션:")
        print("  1. 빈 문자열로 채우기")
        print("  2. 기본값 입력")
        print("  3. 건너뛰기")
        
        choice = input("선택 (1-3): ").strip()
        
        if choice == '1':
            fill_value = ""
            update_null_values(table_name, column_name, fill_value, info['data_type'])
            print(f"✅ '{column_name}' 업데이트 완료")
        elif choice == '2':
            fill_value = input(f"채울 값 입력 ({info['data_type']}): ").strip()
            if fill_value:
                update_null_values(table_name, column_name, fill_value, info['data_type'])
                print(f"✅ '{column_name}' 업데이트 완료")
        else:
            print("⏭️  건너뜀")

def update_null_values(table_name, column_name, fill_value, data_type):
    """NULL 값을 지정된 값으로 업데이트합니다"""
    
    with connection.cursor() as cursor:
        # 값을 올바른 형식으로 포맷
        if data_type in ['integer', 'bigint', 'smallint', 'numeric', 'decimal']:
            if fill_value == "":
                sql_value = "0"
            else:
                sql_value = fill_value
        else:
            sql_value = f"'{fill_value}'"
        
        sql = f"""
            UPDATE "{table_name}" 
            SET "{column_name}" = {sql_value} 
            WHERE "{column_name}" IS NULL
        """
        
        cursor.execute(sql)
        connection.commit()

if __name__ == "__main__":
    null_summary = find_null_values()
    
    if null_summary:
        response = input("\nNULL 값을 채우시겠습니까? (y/n): ").strip().lower()
        if response == 'y':
            fill_null_values_interactive(null_summary)
            print("\n모든 작업이 완료되었습니다!")
        else:
            print("작업을 취소했습니다.")
