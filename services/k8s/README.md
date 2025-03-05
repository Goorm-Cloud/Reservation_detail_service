# Zoochacha 쿠버네티스 배포 가이드

이 디렉토리에는 Zoochacha 예약 상세 서비스를 쿠버네티스에 배포하기 위한 파일들이 포함되어 있습니다.

## 디렉토리 구조

```
services/k8s/
├── app/                    # 애플리케이션 관련 파일
│   ├── Dockerfile          # 애플리케이션 도커 이미지 빌드 파일
│   ├── build.sh            # 애플리케이션 이미지 빌드 스크립트
│   ├── config-template.py  # 설정 파일 템플릿
│   ├── env-template        # 환경 변수 템플릿
│   └── entrypoint.sh       # 컨테이너 시작 스크립트
├── mysql/                  # MySQL 관련 파일
│   ├── Dockerfile          # MySQL 도커 이미지 빌드 파일
│   ├── build.sh            # MySQL 이미지 빌드 스크립트
│   └── my.cnf              # MySQL 설정 파일
├── kubernetes/             # 쿠버네티스 매니페스트 파일
│   ├── app-deployment.yaml # 애플리케이션 배포 매니페스트
│   ├── mysql-statefulset.yaml # MySQL 스테이트풀셋 매니페스트
│   ├── configmap.yaml      # 설정 정보 ConfigMap
│   └── secrets.yaml        # 민감 정보 Secret
├── build_all.sh            # 모든 이미지 빌드 스크립트
└── README.md               # 이 파일
```

## 사전 준비 사항

- Docker 설치
- kubectl 설치
- 쿠버네티스 클러스터 접근 권한

## 도커 이미지 빌드 및 푸시

모든 도커 이미지를 한 번에 빌드하려면:

```bash
./services/k8s/build_all.sh
```

또는 개별적으로 빌드:

```bash
# MySQL 이미지 빌드
./services/k8s/mysql/build.sh

# 애플리케이션 이미지 빌드
./services/k8s/app/build.sh
```

이미지 푸시:

```bash
docker login
docker push zoaba86/zochacha_mysql:v1.0.0
docker push zoaba86/zochacha_reservation_detail:v1.0.0
```

## 쿠버네티스 배포

1. ConfigMap 및 Secret 생성:

```bash
kubectl apply -f services/k8s/kubernetes/configmap.yaml
kubectl apply -f services/k8s/kubernetes/secrets.yaml
```

2. MySQL 스테이트풀셋 배포:

```bash
kubectl apply -f services/k8s/kubernetes/mysql-statefulset.yaml
```

3. 애플리케이션 배포:

```bash
kubectl apply -f services/k8s/kubernetes/app-deployment.yaml
```

## 설정 파일 커스터마이징

`app/config-template.py` 및 `app/env-template` 파일을 참고하여 필요한 설정을 변경할 수 있습니다.
변경된 설정은 ConfigMap 또는 Secret으로 쿠버네티스에 적용해야 합니다.

## 데이터베이스 모드 변경

기본적으로 MySQL을 사용하도록 설정되어 있습니다. SQLite를 사용하려면 환경 변수 `DB_MODE`를 `sqlite`로 설정하세요.

```yaml
env:
  - name: DB_MODE
    value: sqlite
``` 