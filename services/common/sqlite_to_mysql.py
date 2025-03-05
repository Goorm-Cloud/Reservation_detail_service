#!/usr/bin/env python3
import sqlite3
import os
import sys
import datetime

# 현재 디렉토리 기준으로 SQLite DB 파일 경로 설정
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "parking.db")

# 덤프 파일 경로
DUMP_PATH = os.path.join(BASE_DIR, "mysql_dump.sql")

def sqlite_to_mysql_dump():
    """SQLite 데이터베이스를 MySQL 덤프 파일로 변환"""
    
    # SQLite 연결
    try:
        sqlite_conn = sqlite3.connect(DB_PATH)
        sqlite_cursor = sqlite_conn.cursor()
    except Exception as e:
        print(f"SQLite 데이터베이스 연결 오류: {e}")
        sys.exit(1)
    
    # 테이블 목록 가져오기
    sqlite_cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = sqlite_cursor.fetchall()
    
    # 덤프 파일 생성
    with open(DUMP_PATH, 'w', encoding='utf-8') as f:
        # 헤더 정보 추가
        f.write("-- MySQL dump generated from SQLite database\n")
        f.write(f"-- Generated at: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write("-- For Zoochacha Project\n\n")
        
        f.write("SET NAMES utf8mb4;\n")
        f.write("SET FOREIGN_KEY_CHECKS=0;\n\n")
        
        # 각 테이블에 대해 처리
        for table in tables:
            table_name = table[0]
            
            # 시스템 테이블 건너뛰기
            if table_name.startswith('sqlite_') or table_name == 'alembic_version':
                continue
            
            print(f"테이블 처리 중: {table_name}")
            
            # 테이블 스키마 가져오기
            sqlite_cursor.execute(f"PRAGMA table_info({table_name});")
            columns = sqlite_cursor.fetchall()
            
            # CREATE TABLE 문 생성
            f.write(f"DROP TABLE IF EXISTS `{table_name}`;\n")
            f.write(f"CREATE TABLE `{table_name}` (\n")
            
            # 컬럼 정의
            column_defs = []
            primary_keys = []
            
            for col in columns:
                col_id, col_name, col_type, not_null, default_val, is_pk = col
                
                # SQLite 타입을 MySQL 타입으로 변환
                if col_type.upper() == 'INTEGER':
                    mysql_type = 'INT'
                elif col_type.upper() == 'REAL':
                    mysql_type = 'DOUBLE'
                elif col_type.upper().startswith('VARCHAR'):
                    mysql_type = col_type
                elif col_type.upper() == 'BOOLEAN':
                    mysql_type = 'TINYINT(1)'
                elif col_type.upper() == 'DATETIME':
                    mysql_type = 'DATETIME'
                elif col_type.upper() == 'TIME':
                    mysql_type = 'TIME'
                else:
                    mysql_type = 'TEXT'
                
                # 컬럼 정의 생성
                col_def = f"  `{col_name}` {mysql_type}"
                
                if not_null:
                    col_def += " NOT NULL"
                
                if default_val is not None:
                    if default_val == 'CURRENT_TIMESTAMP':
                        col_def += " DEFAULT CURRENT_TIMESTAMP"
                    elif mysql_type == 'TINYINT(1)':
                        col_def += f" DEFAULT {1 if default_val in ('1', 'true', 'True') else 0}"
                    elif mysql_type in ('INT', 'DOUBLE'):
                        col_def += f" DEFAULT {default_val}"
                    else:
                        col_def += f" DEFAULT '{default_val}'"
                
                if is_pk:
                    primary_keys.append(col_name)
                    if mysql_type == 'INT':
                        col_def += " AUTO_INCREMENT"
                
                column_defs.append(col_def)
            
            # 기본 키 추가
            if primary_keys:
                column_defs.append(f"  PRIMARY KEY (`{'`, `'.join(primary_keys)}`)")
            
            f.write(',\n'.join(column_defs))
            f.write("\n) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;\n\n")
            
            # 데이터 가져오기
            sqlite_cursor.execute(f"SELECT * FROM {table_name};")
            rows = sqlite_cursor.fetchall()
            
            if rows:
                # INSERT 문 생성
                f.write(f"LOCK TABLES `{table_name}` WRITE;\n")
                f.write(f"INSERT INTO `{table_name}` VALUES\n")
                
                # 각 행에 대한 VALUES 절 생성
                value_strings = []
                for row in rows:
                    values = []
                    for val in row:
                        if val is None:
                            values.append("NULL")
                        elif isinstance(val, (int, float)):
                            values.append(str(val))
                        elif isinstance(val, bool):
                            values.append("1" if val else "0")
                        else:
                            # 문자열 이스케이프
                            val_str = str(val).replace("'", "''")
                            values.append(f"'{val_str}'")
                    
                    value_strings.append(f"({', '.join(values)})")
                
                f.write(',\n'.join(value_strings))
                f.write(";\n")
                f.write("UNLOCK TABLES;\n\n")
        
        # 외래 키 제약 조건 추가
        f.write("SET FOREIGN_KEY_CHECKS=1;\n")
    
    sqlite_conn.close()
    print(f"MySQL 덤프 파일이 생성되었습니다: {DUMP_PATH}")

if __name__ == "__main__":
    sqlite_to_mysql_dump() 