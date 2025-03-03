FROM python:3.13  
WORKDIR /app

# pandas 등 일부 패키지 빌드를 위한 필수 패키지 설치
RUN apt-get update && apt-get install -y \
    build-essential \
    gcc \
    g++ \
    libffi-dev \
    libssl-dev \
    libpq-dev \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# pip 최신화 후 requirements 설치
COPY requirements.txt requirements.txt
RUN pip install --upgrade pip setuptools wheel && pip install --no-cache-dir -r requirements.txt

# 앱 코드 복사
COPY . .

CMD ["gunicorn", "--bind", "0:5002", "app:create_app()"]

