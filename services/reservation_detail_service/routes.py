from flask import Blueprint
from .reservation_detail_view import reservation_detail, reservation_modify, reservation_delete

reservation_detail_bp = Blueprint('reservation_detail_bp',__name__)

@reservation_detail_bp.route('/<int:reservation_id>', methods=['GET'])
def detail(reservation_id):
    return reservation_detail(reservation_id)

@reservation_detail_bp.route('/<int:reservation_id>', methods=['GET'])
def modify(reservation_id):
    return reservation_modify(reservation_id)

@reservation_detail_bp.route('/<int:reservation_id>', methods=['DELETE'])
def delete(reservation_id):
    return reservation_delete(reservation_id)
