from flask import Blueprint, render_template, request
from services.common.models import db, ParkingLot

parkinglot_bp = Blueprint('parkinglot_bp', __name__)

# ✅ 주차장 목록 페이지 (페이지네이션 추가)
@parkinglot_bp.route('/parking-lots/', methods=['GET'])
def parking_lots():
    page = request.args.get('page', 1, type=int)
    per_page = 8  # 한 페이지당 표시할 주차장 개수
    parking_lots = ParkingLot.query.with_entities(
        ParkingLot.parkinglot_id,
        ParkingLot.parkinglot_name,
        ParkingLot.parkinglot_add,
        ParkingLot.parkinglot_type,
        ParkingLot.parkinglot_cost
    ).paginate(page=page, per_page=per_page, error_out=False)

    return render_template('parking_lots.html', parking_lots=parking_lots)


# ✅ 주차장 상세 페이지 (주차장 ID를 받아 상세 정보 표시)
@parkinglot_bp.route('/parking-lot/<int:parkinglot_id>', methods=['GET'])
def parking_lot_detail(parkinglot_id):
    # 🚀 필요한 필드만 선택하여 가져오기
    parking_lot = db.session.query(
        ParkingLot.parkinglot_id,
        ParkingLot.parkinglot_name,
        ParkingLot.parkinglot_add,
        ParkingLot.parkinglot_type,
        ParkingLot.parkinglot_cost
    ).filter_by(parkinglot_id=parkinglot_id).first()

    if not parking_lot:
        return "주차장을 찾을 수 없습니다.", 404

    return render_template('parking_lot_detail.html', parking_lot=parking_lot)