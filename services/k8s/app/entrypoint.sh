#!/bin/bash
set -e

# 설정 파일 확인
if [ -f "/app/config/config.py" ]; then
    echo "외부 config.py 파일을 사용합니다."
    cp /app/config/config.py /app/config.py
else
    echo "경고: 외부 config.py 파일이 없습니다. 기본 설정을 사용합니다."
fi

# 환경 변수 파일 확인
if [ -f "/app/config/.env" ]; then
    echo "외부 .env 파일을 사용합니다."
    cp /app/config/.env /app/.env
else
    echo "경고: 외부 .env 파일이 없습니다. 기본 환경 변수를 사용합니다."
fi

# 데이터베이스 마이그레이션 실행
echo "데이터베이스 마이그레이션을 실행합니다..."
flask db upgrade

# 애플리케이션 실행
echo "애플리케이션을 시작합니다..."
exec "$@" 