from services.common.models import db, ParkingLot, Reservation, User
from flask import jsonify, render_template, redirect, url_for, request, session, flash
from datetime import datetime


def reservation_detail(reservation_id):

    reservation = Reservation.query.filter_by(reservation_id=reservation_id).first()
    user = User.query.filter_by(user_id=reservation.user_id).first()
    parkinglot = ParkingLot.query.filter_by(parkinglot_id=reservation.parkinglot_id).first()
    
    if not reservation:
        return "예약 정보를 찾을 수 없습니다.", 404

    return render_template('reservation_detail.html', reservation=reservation, user=user, parkingLot=parkinglot)


def reservation_modify(reservation_id):
    # 로그인 체크
    user = session.get('user')
    if not user:  
        return redirect(url_for('login_bp.login_route'))

    # 요청 데이터 확인
    data = request.json
    if not data:
        return jsonify({'error': '요청 데이터가 없습니다.'}), 400

    # 예약 체크
    reservation = Reservation.query.get(reservation_id)
    if not reservation:
        return jsonify({'error': '예약을 찾을 수 없습니다.'}), 404

    # 예약 정보 수정
    if 'reservation_status' in data:
        reservation.reservation_status = data['reservation_status']

    if 'user_name' in data or 'user_email' in data or 'user_phone' in data:
        if not reservation.user:
            return jsonify({'error': '사용자 정보를 찾을 수 없습니다.'}), 404
        if 'user_name' in data:
            reservation.user.name = data['user_name']
        if 'user_email' in data:
            reservation.user.email = data['user_email']
        if 'user_phone' in data:
            reservation.user.phone = data['user_phone']

    if 'modified_by' in data:
        reservation.modified_by = data['modified_by']

    if 'modified_at' in data:
        try:
            reservation.modified_at = datetime.strptime(data['modified_at'], '%Y-%m-%d %H:%M:%S')
        except ValueError:
            return jsonify({'error': 'modified_at 형식이 올바르지 않습니다. (YYYY-MM-DD HH:MM:SS)'}), 400

    db.session.commit()

    return jsonify({'message': '예약 정보가 업데이트되었습니다.'}), 200

def reservation_delete(reservation_id):
  
    reservation = Reservation.query.get(reservation_id)

    if not reservation:
        return "예약을 찾을 수 없습니다.", 404

    if request.method == 'DELETE':
        db.session.delete(reservation)  # 예약 삭제
        db.session.commit()  # 변경 사항 커밋
        flash('삭제되었습니다.', 'success')  # 성공 메시지 추가
        return redirect(url_for('reservation_detail_bp.detail', reservation_id=reservation_id))
