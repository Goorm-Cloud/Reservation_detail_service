FROM python:3.11-slim AS builder

WORKDIR /app

# 빌드 의존성 설치
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# 가상 환경 생성 및 활성화
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# 의존성 설치
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# 실행 단계
FROM python:3.11-slim

# 보안 강화를 위한 비루트 사용자 생성
RUN groupadd -r appuser && useradd -r -g appuser appuser

WORKDIR /app

# 빌더 단계에서 생성된 가상 환경 복사
COPY --from=builder /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# 애플리케이션 코드 복사 (설정 파일 제외)
COPY app.py .
COPY services ./services
COPY templates ./templates
COPY static ./static
COPY migrations ./migrations

# 시작 스크립트 복사
COPY services/k8s/app/entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# 설정 파일 및 민감 정보를 위한 볼륨 마운트 포인트 생성
RUN mkdir -p /app/config
VOLUME ["/app/config"]

# 비루트 사용자로 전환
RUN chown -R appuser:appuser /app
USER appuser

# 포트 설정
EXPOSE 5004

# 환경 변수 설정
ENV PYTHONUNBUFFERED=1
ENV FLASK_APP=app.py

# 시작 스크립트를 ENTRYPOINT로 설정
ENTRYPOINT ["/entrypoint.sh"]

# 애플리케이션 실행
CMD ["gunicorn", "--bind", "0.0.0.0:5004", "-w", "4", "--timeout", "120", "app:create_app()"] 