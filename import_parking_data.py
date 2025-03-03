import os
import sqlite3
from datetime import time
from flask import Flask
from services.common.models import db, ParkingLot

# 앱 생성 및 설정
app = Flask(__name__)
app.config.from_pyfile('config.py')

# DB 초기화
db.init_app(app)

def import_parking_data():
    # 원본 DB 경로
    source_db_path = '/Users/hyunjunson/study/grooming_Project/Zoochacha_monolithic/services/common/parking.db'
    
    with app.app_context():
        try:
            # 원본 DB 연결
            source_conn = sqlite3.connect(source_db_path)
            source_cursor = source_conn.cursor()
            
            # 주차장 테이블 데이터 조회
            source_cursor.execute("SELECT * FROM parkinglot")
            parking_lots = source_cursor.fetchall()
            
            # 컬럼명 가져오기
            column_names = [description[0] for description in source_cursor.description]
            
            # 데이터를 딕셔너리 형태로 변환
            parking_lot_dicts = []
            for row in parking_lots:
                parking_lot_dict = {}
                for i, column_name in enumerate(column_names):
                    parking_lot_dict[column_name] = row[i]
                parking_lot_dicts.append(parking_lot_dict)
            
            # 원본 DB 연결 종료
            source_conn.close()
            
            # 기존 주차장 데이터 삭제 (기존 예약 데이터는 유지)
            # 외래 키 제약 조건 때문에 삭제하지 않고 업데이트 방식으로 진행
            existing_parking_lots = ParkingLot.query.all()
            existing_ids = {p.parkinglot_id for p in existing_parking_lots}
            
            # 새로운 주차장 데이터 추가 또는 업데이트
            for parking_lot_data in parking_lot_dicts:
                parking_id = parking_lot_data.get('parkinglot_id')
                
                # 시간 데이터 처리
                parkinglot_time_value = parking_lot_data.get('parkinglot_time')
                if parkinglot_time_value is not None and not isinstance(parkinglot_time_value, time):
                    if isinstance(parkinglot_time_value, int):
                        # 정수 값을 시간으로 변환 (초 단위로 가정)
                        hours = parkinglot_time_value // 3600
                        minutes = (parkinglot_time_value % 3600) // 60
                        seconds = parkinglot_time_value % 60
                        parkinglot_time_value = time(hour=hours, minute=minutes, second=seconds)
                    else:
                        # 시간 데이터가 없거나 변환할 수 없는 경우 None으로 설정
                        parkinglot_time_value = None
                
                # 기존 ID가 있으면 업데이트, 없으면 새로 추가
                existing_parking = ParkingLot.query.filter_by(parkinglot_id=parking_id).first()
                
                if existing_parking:
                    # 기존 데이터 업데이트
                    existing_parking.parkinglot_name = parking_lot_data.get('parkinglot_name')
                    existing_parking.latitude = parking_lot_data.get('latitude')
                    existing_parking.longitude = parking_lot_data.get('longitude')
                    existing_parking.parkinglot_div = parking_lot_data.get('parkinglot_div')
                    existing_parking.parkinglot_type = parking_lot_data.get('parkinglot_type')
                    existing_parking.parkinglot_num = parking_lot_data.get('parkinglot_num')
                    existing_parking.parkinglot_cost = parking_lot_data.get('parkinglot_cost')
                    existing_parking.parkinglot_add = parking_lot_data.get('parkinglot_add')
                    existing_parking.parkinglot_day = parking_lot_data.get('parkinglot_day')
                    existing_parking.parkinglot_time = parkinglot_time_value
                else:
                    # 새 데이터 추가
                    new_parking = ParkingLot(
                        parkinglot_id=parking_id,
                        parkinglot_name=parking_lot_data.get('parkinglot_name'),
                        latitude=parking_lot_data.get('latitude'),
                        longitude=parking_lot_data.get('longitude'),
                        parkinglot_div=parking_lot_data.get('parkinglot_div'),
                        parkinglot_type=parking_lot_data.get('parkinglot_type'),
                        parkinglot_num=parking_lot_data.get('parkinglot_num'),
                        parkinglot_cost=parking_lot_data.get('parkinglot_cost'),
                        parkinglot_add=parking_lot_data.get('parkinglot_add'),
                        parkinglot_day=parking_lot_data.get('parkinglot_day'),
                        parkinglot_time=parkinglot_time_value
                    )
                    db.session.add(new_parking)
            
            db.session.commit()
            print(f"주차장 데이터 {len(parking_lot_dicts)}개를 성공적으로 가져왔습니다.")
            
        except Exception as e:
            print(f"주차장 데이터 가져오기 중 오류 발생: {e}")
            db.session.rollback()

if __name__ == "__main__":
    import_parking_data() 