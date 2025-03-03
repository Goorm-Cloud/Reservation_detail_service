from flask import Blueprint, render_template, request, jsonify, redirect, url_for, flash, session
from datetime import datetime
from services.common.models import db, User, ParkingLot, Reservation

reservation_detail_bp = Blueprint('reservation_detail_bp', __name__)

@reservation_detail_bp.route('/<int:reservation_id>', methods=['GET', 'POST', 'PATCH', 'DELETE'])
def modify(reservation_id):
    # GET 요청 처리 (상세 정보 표시)
    if request.method == 'GET':
        print(f"예약 상세 조회: {reservation_id}")
        
        reservation = Reservation.query.filter_by(reservation_id=reservation_id).first()
        
        if not reservation:
            return redirect(url_for('reservation_detail_bp.not_found'))
        
        # 삭제된 예약이지만 취소 상태인 경우 표시
        if reservation.is_deleted and reservation.reservation_status != 'cancel':
            return redirect(url_for('reservation_detail_bp.not_found'))
            
        user = User.query.filter_by(user_id=reservation.user_id).first()
        parkinglot = ParkingLot.query.filter_by(parkinglot_id=reservation.parkinglot_id).first()
        
        if not user or not parkinglot:
            return redirect(url_for('reservation_detail_bp.not_found'))

        return render_template('reservation_detail.html', reservation=reservation, user=user, parkinglot=parkinglot)
    
    # POST 또는 PATCH 요청 처리 (정보 수정)
    elif request.method == 'POST' or request.method == 'PATCH':
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
                return redirect(url_for('reservation_detail_bp.modify', reservation_id=reservation_id))
            
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
            return redirect(url_for('reservation_detail_bp.modify', reservation_id=reservation_id, _t=timestamp))
            
        except Exception as e:
            db.session.rollback()
            print(f"오류 발생: {str(e)}")
            flash(f'오류가 발생했습니다: {str(e)}', 'error')
            return redirect(url_for('reservation_detail_bp.modify', reservation_id=reservation_id))
    
    # DELETE 요청 처리
    elif request.method == 'DELETE':
        try:
            # 예약 체크
            reservation = Reservation.query.filter_by(reservation_id=reservation_id).first()
            if not reservation:
                return jsonify({'success': False, 'message': '예약을 찾을 수 없습니다.'}), 404
            
            # 예약 상태를 'cancel'로 변경하고 is_deleted 필드를 True로 설정
            reservation.reservation_status = 'cancel'
            reservation.is_deleted = True
            reservation.modified_at = datetime.utcnow()
            reservation.modified_by = "시스템(삭제)"
            db.session.commit()
            
            # 성공 응답과 함께 리다이렉트할 URL 전송
            return jsonify({
                'success': True, 
                'message': '예약이 취소되었습니다.',
                'redirect_url': url_for('reservation_detail_bp.modify', reservation_id=reservation_id)
            }), 200
        except Exception as e:
            db.session.rollback()
            print(f"삭제 오류 발생: {str(e)}")
            return jsonify({'success': False, 'message': f'오류가 발생했습니다: {str(e)}'}), 500
    
    # 다른 메서드 요청
    return jsonify({'success': False, 'message': '잘못된 요청입니다.'}), 400

# 기존 detail 라우트를 리다이렉트로 변경
@reservation_detail_bp.route('/detail/<int:reservation_id>', methods=['GET'])
def detail(reservation_id):
    return redirect(url_for('reservation_detail_bp.modify', reservation_id=reservation_id))

@reservation_detail_bp.route('/not-found', methods=['GET'])
def not_found():
    """
    예약 정보가 없을 때 보여줄 화면
    """
    return render_template('reservation_not_found.html')

# API 엔드포인트 추가
@reservation_detail_bp.route('/api/detail/<int:reservation_id>', methods=['GET'])
def api_detail(reservation_id):
    # 취소된 예약도 포함하여 조회
    reservation = Reservation.query.filter_by(reservation_id=reservation_id).first()
    
    if not reservation:
        return jsonify({'success': False, 'message': '예약을 찾을 수 없습니다.'}), 404
    
    # 삭제된 예약이지만 취소 상태가 아닌 경우 표시하지 않음
    if reservation.is_deleted and reservation.reservation_status != 'cancel':
        return jsonify({'success': False, 'message': '예약을 찾을 수 없습니다.'}), 404
        
    user = User.query.filter_by(user_id=reservation.user_id).first()
    parkinglot = ParkingLot.query.filter_by(parkinglot_id=reservation.parkinglot_id).first()
    
    if not user or not parkinglot:
        return jsonify({'success': False, 'message': '사용자 또는 주차장 정보를 찾을 수 없습니다.'}), 404

    reservation_data = {
        'reservation_id': reservation.reservation_id,
        'parkinglot_id': reservation.parkinglot_id,
        'parkinglot_name': parkinglot.parkinglot_name,
        'user_id': reservation.user_id,
        'user_name': user.name,
        'user_email': user.email,
        'user_phone': user.phone,
        'reservation_status': reservation.reservation_status,
        'is_deleted': reservation.is_deleted,
        'created_at': reservation.created_at.isoformat() if reservation.created_at else None,
        'modified_at': reservation.modified_at.isoformat() if reservation.modified_at else None
    }
    
    return jsonify({'success': True, 'data': reservation_data})

@reservation_detail_bp.route('/reactivate/<int:reservation_id>', methods=['POST'])
def reactivate(reservation_id):
    """
    취소된 예약을 다시 활성화하는 기능
    """
    try:
        # 예약 체크
        reservation = Reservation.query.filter_by(reservation_id=reservation_id).first()
        if not reservation:
            return jsonify({'success': False, 'message': '예약을 찾을 수 없습니다.'}), 404
        
        # 예약 상태를 'confirm'으로 변경하고 is_deleted 필드를 False로 설정
        reservation.reservation_status = 'confirm'
        reservation.is_deleted = False
        reservation.modified_at = datetime.utcnow()
        reservation.modified_by = "시스템(재예약)"
        db.session.commit()
        
        # 성공 응답과 함께 리다이렉트할 URL 전송
        return jsonify({
            'success': True, 
            'message': '예약이 재활성화되었습니다.',
            'redirect_url': url_for('reservation_detail_bp.modify', reservation_id=reservation_id)
        }), 200
    except Exception as e:
        db.session.rollback()
        print(f"재예약 오류 발생: {str(e)}")
        return jsonify({'success': False, 'message': f'오류가 발생했습니다: {str(e)}'}), 500