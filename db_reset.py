import os
import random
import string
from datetime import datetime, timedelta
from flask import Flask
from services.common.models import db, User, ParkingLot, Reservation

# 앱 생성 및 설정
app = Flask(__name__)
app.config.from_pyfile('config.py')

# DB 초기화
db.init_app(app)

# 한글 이름 생성을 위한 성과 이름 목록
LAST_NAMES = ['김', '이', '박', '최', '정', '강', '조', '윤', '장', '임', '한', '오', '서', '신', '권', '황', '안', '송', '전', '홍']
FIRST_NAMES = ['민준', '서준', '도윤', '예준', '시우', '하준', '지호', '준서', '준우', '민서', 
               '현우', '지훈', '지민', '지우', '지현', '지영', '지원', '지수', '지은', '지혜',
               '서연', '서윤', '지민', '서현', '민서', '하은', '하윤', '윤서', '지우', '채원']

# 성별 목록
GENDERS = ['남성', '여성']

# 랜덤 전화번호 생성 함수
def generate_phone():
    return f"010-{random.randint(1000, 9999)}-{random.randint(1000, 9999)}"

# 랜덤 이메일 생성 함수
def generate_email(name):
    domains = ['gmail.com', 'naver.com', 'daum.net', 'kakao.com', 'yahoo.com']
    username = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
    return f"{username}@{random.choice(domains)}"

# 랜덤 날짜 생성 함수
def generate_date(start_date=datetime(2023, 1, 1), end_date=datetime.now()):
    delta = end_date - start_date
    random_days = random.randint(0, delta.days)
    random_seconds = random.randint(0, 24*60*60)
    return start_date + timedelta(days=random_days, seconds=random_seconds)

def reset_database():
    with app.app_context():
        # 기존 테이블 삭제 및 새로 생성
        db.drop_all()
        db.create_all()
        
        # 기존 주차장 데이터 백업
        parking_lots = []
        try:
            # 기존 DB에서 주차장 데이터 가져오기
            conn = db.engine.connect()
            result = conn.execute("SELECT * FROM parkinglot")
            for row in result:
                parking_lot = {}
                for column in result.keys():
                    parking_lot[column] = row[column]
                parking_lots.append(parking_lot)
            conn.close()
        except Exception as e:
            print(f"주차장 데이터 백업 중 오류 발생: {e}")
            # 주차장 데이터가 없는 경우 샘플 데이터 생성
            for i in range(1, 21):
                parking_lot = ParkingLot(
                    parkinglot_name=f"샘플 주차장 {i}",
                    latitude=str(37.5 + random.random() * 0.1),
                    longitude=str(127.0 + random.random() * 0.1),
                    parkinglot_div="public" if random.random() > 0.5 else "private",
                    parkinglot_type=random.choice(["indoor", "outdoor", "attached"]),
                    parkinglot_num=random.randint(10, 100),
                    parkinglot_cost=random.random() > 0.5,
                    parkinglot_add=f"서울시 강남구 테헤란로 {random.randint(1, 100)}길 {random.randint(1, 50)}",
                    parkinglot_day=random.choice(["mon", "tue", "wed", "thu", "fri", "sat", "sun"]),
                    parkinglot_time=datetime.strptime(f"{random.randint(0, 23)}:00:00", "%H:%M:%S").time()
                )
                db.session.add(parking_lot)
            db.session.commit()
            
            # 생성된 주차장 데이터 가져오기
            parking_lots = ParkingLot.query.all()
        
        # 주차장 데이터 복원
        if parking_lots:
            for parking_lot_data in parking_lots:
                if isinstance(parking_lot_data, dict):
                    # 딕셔너리인 경우 (백업 데이터)
                    parking_lot = ParkingLot(
                        parkinglot_id=parking_lot_data.get('parkinglot_id'),
                        parkinglot_name=parking_lot_data.get('parkinglot_name'),
                        latitude=parking_lot_data.get('latitude'),
                        longitude=parking_lot_data.get('longitude'),
                        parkinglot_div=parking_lot_data.get('parkinglot_div'),
                        parkinglot_type=parking_lot_data.get('parkinglot_type'),
                        parkinglot_num=parking_lot_data.get('parkinglot_num'),
                        parkinglot_cost=parking_lot_data.get('parkinglot_cost'),
                        parkinglot_add=parking_lot_data.get('parkinglot_add'),
                        parkinglot_day=parking_lot_data.get('parkinglot_day'),
                        parkinglot_time=parking_lot_data.get('parkinglot_time')
                    )
                    db.session.add(parking_lot)
            db.session.commit()
        
        # 사용자 데이터 생성 (50명)
        for i in range(1, 51):
            last_name = random.choice(LAST_NAMES)
            first_name = random.choice(FIRST_NAMES)
            full_name = last_name + first_name
            gender = random.choice(GENDERS)
            
            user = User(
                name=full_name,
                gender=gender,
                email=generate_email(full_name),
                age=random.randint(20, 60),
                phone=generate_phone(),
                role="user"
            )
            db.session.add(user)
        db.session.commit()
        
        # 예약 데이터 생성 (100개)
        users = User.query.all()
        parking_lots = ParkingLot.query.all()
        
        for i in range(1, 101):
            user = random.choice(users)
            parking_lot = random.choice(parking_lots)
            created_date = generate_date()
            
            reservation = Reservation(
                user_id=user.user_id,
                parkinglot_id=parking_lot.parkinglot_id,
                reservation_status=random.choice(["confirm", "none", "cancel"]),
                is_deleted=False,
                created_at=created_date,
                created_by=user.name,
                modified_at=created_date,
                modified_by=user.name
            )
            db.session.add(reservation)
        db.session.commit()
        
        print("데이터베이스 초기화 및 데이터 생성이 완료되었습니다.")

if __name__ == "__main__":
    reset_database() 