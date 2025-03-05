#!/bin/bash
set -e

# 스크립트 디렉토리 경로
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "===== Zoochacha 도커 이미지 빌드 스크립트 ====="

# MySQL 이미지 빌드
echo -e "\n[1/2] MySQL 이미지 빌드 시작..."
bash "$SCRIPT_DIR/mysql/build.sh"

# 애플리케이션 이미지 빌드
echo -e "\n[2/2] 애플리케이션 이미지 빌드 시작..."
bash "$SCRIPT_DIR/app/build.sh"

echo -e "\n===== 모든 도커 이미지 빌드 완료 ====="
echo "빌드된 이미지:"
echo "- zoaba86/zochacha_mysql:v1.0.0"
echo "- zoaba86/zochacha_reservation_detail:v1.0.0"
echo -e "\n이미지를 푸시하려면 다음 명령어를 실행하세요:"
echo "docker login"
echo "docker push zoaba86/zochacha_mysql:v1.0.0"
echo "docker push zoaba86/zochacha_reservation_detail:v1.0.0" 