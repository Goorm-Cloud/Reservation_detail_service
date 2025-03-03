import os
import json
from flask import url_for, render_template, redirect, request, Response, send_from_directory, jsonify
from services.common.models import db, Reservation, ParkingLot, User
from datetime import datetime
from services.reservation_service.reservation_form import ReservationForm
from flask import flash


# 📌 정적 파일 제공
def static_files(filename):
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    STATIC_DIR = os.path.join(BASE_DIR, "reservation_service", "static")
    return send_from_directory(STATIC_DIR, filename)

# 📌 주차장 예약 처리

def reserve_parking(parkinglot_id):
    """
    선택한 주차장 예약 페이지 로드 및 예약 처리
    """
    parking_lot = db.session.query(
        ParkingLot.parkinglot_id,
        ParkingLot.parkinglot_name,
        ParkingLot.parkinglot_add
    ).filter_by(parkinglot_id=parkinglot_id).first()

    if not parking_lot:
        return jsonify({"success": False, "message": "❌ 주차장을 찾을 수 없습니다."}), 404

    form = ReservationForm()

    if form.validate_on_submit():  # ✅ FlaskForm 검증 추가
        email = form.email.data  # FlaskForm에서 입력 데이터 가져오기

        # 🚀 이메일로 사용자 조회
        user = db.session.query(User).filter_by(email=email).first()

        if not user:
            flash("❌ 등록되지 않은 사용자입니다. 이메일을 확인하세요.", "danger")
            return render_template('reserve_parking.html', parking_lot=parking_lot, form=form)

        # 🚀 예약 생성
        new_reservation = Reservation(
            user_id=user.user_id,
            parkinglot_id=parkinglot_id,
            reservation_status="confirm",
            created_at=datetime.utcnow(),
            created_by=str(user.name),
            modified_at=datetime.utcnow(),
            modified_by=str(user.name)
        )

        db.session.add(new_reservation)
        db.session.commit()

        # 예약 상세 페이지로 리다이렉트
        return redirect(url_for('reservation_detail_bp.detail', reservation_id=new_reservation.reservation_id))

    return render_template('reserve_parking.html', parking_lot=parking_lot, form=form)