from flask import Flask
from services.common.models import db, ParkingLot, Reservation
import random

# 앱 생성 및 설정
app = Flask(__name__)
app.config.from_pyfile('config.py')

# DB 초기화
db.init_app(app)

def delete_sample_parking_data():
    """
    1~20번 주차장 데이터를 삭제하는 함수
    """
    with app.app_context():
        try:
            # 1~20번 주차장 데이터 조회
            sample_parking_lots = ParkingLot.query.filter(
                ParkingLot.parkinglot_id.between(1, 20)
            ).all()
            
            if not sample_parking_lots:
                print("삭제할 샘플 주차장 데이터가 없습니다.")
                return
            
            # 삭제할 주차장 ID 목록
            parking_ids = [p.parkinglot_id for p in sample_parking_lots]
            print(f"삭제할 주차장 ID: {parking_ids}")
            
            # 대체할 주차장 ID 목록 (10000번 이상의 주차장)
            alternative_parking_lots = ParkingLot.query.filter(
                ParkingLot.parkinglot_id >= 10000
            ).limit(100).all()
            
            if not alternative_parking_lots:
                print("대체할 주차장 데이터가 없습니다.")
                return
            
            alternative_parking_ids = [p.parkinglot_id for p in alternative_parking_lots]
            
            # 1~20번 주차장을 참조하는 예약 데이터 조회
            reservations = Reservation.query.filter(
                Reservation.parkinglot_id.in_(parking_ids)
            ).all()
            
            if reservations:
                print(f"{len(reservations)}개의 예약 데이터가 1~20번 주차장을 참조하고 있습니다.")
                
                # 예약 데이터의 주차장 ID를 대체 주차장 ID로 변경
                for reservation in reservations:
                    # 랜덤하게 대체 주차장 선택
                    new_parking_id = random.choice(alternative_parking_ids)
                    print(f"예약 ID {reservation.reservation_id}: 주차장 ID {reservation.parkinglot_id} -> {new_parking_id}")
                    reservation.parkinglot_id = new_parking_id
                
                db.session.commit()
                print(f"{len(reservations)}개의 예약 데이터가 업데이트되었습니다.")
            
            # 주차장 데이터 삭제
            for parking_lot in sample_parking_lots:
                db.session.delete(parking_lot)
            
            db.session.commit()
            print(f"{len(sample_parking_lots)}개의 샘플 주차장 데이터가 삭제되었습니다.")
            
        except Exception as e:
            print(f"주차장 데이터 삭제 중 오류 발생: {e}")
            db.session.rollback()

if __name__ == "__main__":
    delete_sample_parking_data() 