#!/bin/bash
set -e

# 스크립트 디렉토리 경로
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../../.." && pwd)"

# MySQL 덤프 파일 생성
echo "SQLite에서 MySQL 덤프 파일 생성 중..."
cd "$PROJECT_ROOT"
python -m services.common.sqlite_to_mysql

# 덤프 파일 복사
echo "MySQL 덤프 파일 복사 중..."
cp "$PROJECT_ROOT/services/common/mysql_dump.sql" "$SCRIPT_DIR/"

# 도커 이미지 빌드
echo "MySQL 도커 이미지 빌드 중..."
cd "$SCRIPT_DIR"
docker build -t zoaba86/zochacha_mysql:v1.0.0 .

echo "MySQL 도커 이미지 빌드 완료: zoaba86/zochacha_mysql:v1.0.0"
echo "이미지를 푸시하려면 다음 명령어를 실행하세요:"
echo "docker login"
echo "docker push zoaba86/zochacha_mysql:v1.0.0" 