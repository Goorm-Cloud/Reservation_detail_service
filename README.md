Zoochacha_monolithic/
│── services/   # 서비스 패키지
│   │── admin_service/               # 1- 관리자 서비스
│   │   │── views/                   # 관리자 서비스 뷰 및 컨트롤러
│   │   │   │── admin_list.py
│   │   │   │── parkinglot.py
│   │   │   │── reservation.py
│   │   │── __init__.py
│   │   │── routes.py                # 관리자 서비스 라우트 설정
│   │   │── Dockerfile               # 관리자 서비스 컨테이너 빌드 파일
│   │   │── requirements.txt         # 관리자 서비스 패키지 종속성 목록
│   │
│   │── map_service/                 # 2 - 지도 관련 서비스 (내부 구조 동일)
│   │── reservation_service/         # 3 - 예약 서비스 (내부 구조 동일)
│   │── reservation_detail_service/  # 4 - 예약 상세 서비스 (내부 구조 동일)
│   │── k8s/  # Kubernetes 관련 설정
│
│── common/    # 공통 모듈
│   │── database.py  # SQLAlchemy 데이터베이스 설정
│   │── models.py    # 데이터베이스 모델
│   │── oauth.py     # OAuth 인증 관련
│   │── parking.db   # 공유 데이터베이스 파일(임시. SQLite)
│
│── static/     # 정적 파일 (CSS, JS, 이미지 등)
│── templates/  # Jinja2 기반 HTML 템플릿
│── .env        # 환경 변수 파일
│── .gitignore  # Git 제외 파일 목록
│── app.py      # Flask 애플리케이션 실행 엔트리 포인트
│── config.py   # 애플리케이션 설정 파일
│── run.py      # 앱 실행을 위한 별도 스크립트
