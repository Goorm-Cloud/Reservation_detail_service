from services.common.models import db, ParkingLot, Reservation, User
from flask import jsonify, render_template, redirect, url_for, request, session, flash
from datetime import datetime


def reservation_detail(reservation_id):

    reservation = Reservation.query.filter_by(reservation_id=reservation_id).first()
    
    if not reservation:
        return redirect(url_for('reservation_detail_bp.not_found'))
    
    # 삭제된 예약은 표시하지 않음
    if reservation.is_deleted:
        return redirect(url_for('reservation_detail_bp.not_found'))
        
    user = User.query.filter_by(user_id=reservation.user_id).first()
    parkinglot = ParkingLot.query.filter_by(parkinglot_id=reservation.parkinglot_id).first()
    
    if not user or not parkinglot:
        return redirect(url_for('reservation_detail_bp.not_found'))

    return render_template('reservation_detail.html', reservation=reservation, user=user, parkinglot=parkinglot)


def reservation_modify(reservation_id):
    # 요청 데이터 확인
    if request.method == 'POST' or request.method == 'PATCH':
        # 폼 데이터 처리
        try:
            # 디버깅용 로그
            print("===== 폼 데이터 시작 =====")
            print(f"폼 데이터: {request.form}")
            print(f"전화번호: {request.form.get('user_phone')}")
            print(f"이메일: {request.form.get('user_email')}")
            print("===== 폼 데이터 끝 =====")
            
            # 예약 체크
            reservation = Reservation.query.filter_by(reservation_id=reservation_id).first()
            if not reservation:
                flash('예약을 찾을 수 없습니다.', 'error')
                return redirect(url_for('reservation_detail_bp.not_found'))

            # 사용자 정보 체크
            user = User.query.filter_by(user_id=reservation.user_id).first()
            if not user:
                flash('사용자 정보를 찾을 수 없습니다.', 'error')
                return redirect(url_for('reservation_detail_bp.detail', reservation_id=reservation_id))
            
            # 기존 정보 출력
            print(f"수정 전 - 전화번호: {user.phone}, 이메일: {user.email}")
            
            # 예약 정보 수정
            current_time = datetime.utcnow()
            reservation.modified_at = current_time
            reservation.modified_by = "시스템(수정)"
            
            # 폼 데이터에서 필요한 정보 추출 및 업데이트
            if request.form.get('reservation_status'):
                reservation.reservation_status = request.form.get('reservation_status')
            
            # 전화번호 수정
            phone = request.form.get('user_phone')
            if phone:
                user.phone = phone
                print(f"전화번호 수정: {phone}")
            
            # 이메일 수정
            email = request.form.get('user_email')
            if email:
                user.email = email
                print(f"이메일 수정: {email}")
            
            # 변경사항 저장
            db.session.commit()
            print(f"수정 후 - 전화번호: {user.phone}, 이메일: {user.email}")
            
            # 성공 메시지 추가
            flash('예약 정보가 성공적으로 업데이트되었습니다.', 'success')
            
            # 상세 페이지로 리다이렉트 (캐시 방지를 위한 타임스탬프 추가)
            timestamp = int(datetime.utcnow().timestamp())
            return redirect(url_for('reservation_detail_bp.detail', reservation_id=reservation_id, _t=timestamp))
            
        except Exception as e:
            db.session.rollback()
            print(f"오류 발생: {str(e)}")
            flash(f'오류가 발생했습니다: {str(e)}', 'error')
            return redirect(url_for('reservation_detail_bp.detail', reservation_id=reservation_id))
    
    # GET 요청인 경우 상세 페이지로 리다이렉트
    return redirect(url_for('reservation_detail_bp.detail', reservation_id=reservation_id))

def reservation_delete(reservation_id):
    # DELETE 요청 처리
    if request.method == 'DELETE':
        try:
            # 예약 체크
            reservation = Reservation.query.filter_by(reservation_id=reservation_id).first()
            if not reservation:
                return jsonify({'success': False, 'message': '예약을 찾을 수 없습니다.'}), 404
            
            # 실제 삭제 대신 is_deleted 필드를 True로 설정
            reservation.is_deleted = True
            reservation.modified_at = datetime.utcnow()
            reservation.modified_by = "시스템(삭제)"
            db.session.commit()
            
            return jsonify({'success': True, 'message': '예약이 삭제되었습니다.'}), 200
        except Exception as e:
            db.session.rollback()
            print(f"삭제 오류 발생: {str(e)}")
            return jsonify({'success': False, 'message': f'오류가 발생했습니다: {str(e)}'}), 500
    
    # DELETE 요청이 아닌 경우
    return jsonify({'success': False, 'message': '잘못된 요청입니다.'}), 400

def reservation_not_found():
    """
    예약 정보가 없을 때 보여줄 화면
    """
    return render_template('reservation_not_found.html')
