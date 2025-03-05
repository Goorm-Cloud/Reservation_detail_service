#!/bin/bash
set -e

# 스크립트 디렉토리 경로
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../../.." && pwd)"

# 도커 이미지 빌드
echo "애플리케이션 도커 이미지 빌드 중..."
cd "$PROJECT_ROOT"
docker build -t zoaba86/zochacha_reservation_detail:v1.0.0 -f services/k8s/app/Dockerfile .

echo "애플리케이션 도커 이미지 빌드 완료: zoaba86/zochacha_reservation_detail:v1.0.0"
echo "이미지를 푸시하려면 다음 명령어를 실행하세요:"
echo "docker login"
echo "docker push zoaba86/zochacha_reservation_detail:v1.0.0" 