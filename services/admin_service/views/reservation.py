from flask import render_template, redirect, url_for, request, session, flash
from services.common.models import db, Reservation
from datetime import datetime

# Deprecated
def add_reservation():
    # if request.method == 'POST':
    #     # 새로운 예약 객체 생성
    #     new_reservation = Reservation(
    #         name=request.form['name'],
    #         car_number=request.form['car_number'],
    #         date=request.form['date'],
    #         time=request.form['time'],
    #     )
    #     # DB에 새 예약 추가
    #     db.session.add(new_reservation)
    #     db.session.commit()  # 변경 사항 커밋
    #     return redirect(url_for('admin.admin_dashboard'))

    return render_template('add_reservation.html')


def edit_reservation(reservation_id):

    # 로그인 체크
    user = session.get('user')
    if not user:  
        return redirect(url_for('login_bp.login_route'))

    # 예약 체크
    reservation = Reservation.query.get(reservation_id)
    if not reservation:
        return "예약을 찾을 수 없습니다.", 404

    # 예약 수정
    if request.method == 'POST':
        reservation.user_id = request.form['user_id']
        reservation.reservation_status = request.form['reservation_status']
        reservation.modified_at = datetime.utcnow()  # 수정일시
        reservation.modified_by = session.get('user').get('name')#request.form['user_id']  # 수정자 ID
        db.session.commit()  # 변경 사항 커밋

        reservation.user_id = request.form['user_id']
        reservation.parkinglot_id = request.form['parkinglot_id']
        reservation.reservation_status = request.form.get('reservation_status',
                                                          reservation.reservation_status)  
        reservation.modified_at = datetime.now()
        reservation.modified_by = user.get('sub')  # 현재 로그인된 사용자 ID
        db.session.commit()

        return redirect(url_for('admin_bp.reservation_detail_route', reservation_id=reservation_id))

    return render_template('edit_reservation.html', reservation=reservation)


def delete_reservation(reservation_id):
    reservation = Reservation.query.get(reservation_id)

    if not reservation:
        return "예약을 찾을 수 없습니다.", 404

    if request.method == 'POST':
        db.session.delete(reservation)  # 예약 삭제
        db.session.commit()  # 변경 사항 커밋
        flash('삭제되었습니다.', 'success')  # 성공 메시지 추가
        return redirect(url_for('admin_bp.admin_dashboard_route'))

    return render_template('delete_reservation.html', reservation=reservation)


def reservation_detail(reservation_id):
    # reservation_id에 해당하는 예약을 DB에서 찾음
    reservation = Reservation.query.get(reservation_id)

    if reservation is None:
        return "예약을 찾을 수 없습니다.", 404

    return render_template('admin_reservation_detail.html', reservation=reservation)
