from flask import Blueprint, render_template, request, redirect, url_for, flash
from services.common.models import db, Reservation, ParkingLot, User
from datetime import datetime

reservation_bp = Blueprint('reservation_bp', __name__)


# ✅ 예약 페이지 (GET: 예약 폼 렌더링, POST: DB 저장)
@reservation_bp.route('/parking-lot/<int:parkinglot_id>/reserve', methods=['GET', 'POST'])
def reserve_parking(parkinglot_id):
    print("🚀 parkinglot_id: ", parkinglot_id)
    # 🚀 필요한 필드만 가져오기
    parking_lot = db.session.query(
        ParkingLot.parkinglot_id,
        ParkingLot.parkinglot_name,
        ParkingLot.parkinglot_add
    ).filter_by(parkinglot_id=parkinglot_id).first()

    if not parking_lot:
        return "주차장을 찾을 수 없습니다.", 404

    if request.method == 'POST':
        email = request.form.get("email")  # 사용자 이메일 입력 받기

        # 🚀 이메일로 사용자 조회
        user = db.session.query(User).filter_by(email=email).first()

        if not user:
            flash("등록되지 않은 유저 정보입니다. 올바른 이메일을 입력하세요.", "danger")
            return redirect(url_for('reservation.reserve_parking', parkinglot_id=parkinglot_id))

        # 🚀 `reservation_status`를 "confirm"으로 설정하고 예약 생성
        new_reservation = Reservation(
            user_id=user.user_id,  # 이메일로 찾은 유저의 ID 사용
            parkinglot_id=parkinglot_id,
            reservation_status="confirm",
            modified_at=datetime.utcnow(),  # ✅ DATETIME → TEXT 변환 후 저장
            modified_by=str(user.user_id)
        )

        db.session.add(new_reservation)
        db.session.commit()

        flash("예약이 성공적으로 완료되었습니다!", "success")
        return redirect(url_for('parkinglot.parking_lots'))  # ✅ 주차장 목록으로 이동

    return render_template('reserve_parking.html', parking_lot=parking_lot)