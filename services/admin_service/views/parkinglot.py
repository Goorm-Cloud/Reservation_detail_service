from flask import render_template, redirect, url_for, request
from sqlalchemy.orm import defer
from services.common.models import db, ParkingLot
import os

# 주차장 정보 수정
def edit_parkinglot(parkinglot_id):

    # parkinglot_time 제외한 ORM 객체 가져옴 (모델 수정 필요)
    parkinglot = ParkingLot.query.options(defer(ParkingLot.parkinglot_time)) \
        .filter_by(parkinglot_id=parkinglot_id).first()

    if not parkinglot:
        return "주차장을 찾을 수 없습니다.", 404

    # 예약 수정
    if request.method == 'POST':
        parkinglot.parkinglot_name = request.form['parkinglot_name']
        parkinglot.latitude = request.form['latitude']
        parkinglot.longitude = request.form['longitude']
        parkinglot.parkinglot_div = request.form['parkinglot_div']
        parkinglot.parkinglot_type = request.form['parkinglot_type']
        parkinglot.parkinglot_num = request.form['parkinglot_num']
        parkinglot.parkinglot_add = request.form['parkinglot_add']
        db.session.commit()  # 변경 사항 커밋
        return redirect(url_for('admin_bp.edit_parkinglot_route', parkinglot_id=parkinglot_id))

    return render_template('edit_parkinglot.html', parkinglot=parkinglot)

# 주차장 지도 보기, 검색
def admin_parkinglot():
    print("✅ admin_parkinglot 호출")
    kakao_api_key = os.getenv("KAKAO_API_KEY")
    return render_template("admin_parkinglot.html", kakao_api_key=kakao_api_key)
