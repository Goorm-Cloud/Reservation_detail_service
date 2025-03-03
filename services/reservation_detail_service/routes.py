from flask import Blueprint, render_template, request
from .views.reservation_detail_view import reservation_detail, reservation_modify, reservation_delete, reservation_not_found

reservation_detail_bp = Blueprint('reservation_detail_bp',__name__)

@reservation_detail_bp.route('/detail/<int:reservation_id>', methods=['GET'])
def detail(reservation_id):
    print(reservation_id)
    return reservation_detail(reservation_id)

@reservation_detail_bp.route('/<int:reservation_id>', methods=['GET', 'POST', 'PATCH'])
def modify(reservation_id):
    if request.method == 'POST' or request.method == 'PATCH':
        return reservation_modify(reservation_id)
    else:
        return reservation_detail(reservation_id)

@reservation_detail_bp.route('/<int:reservation_id>', methods=['DELETE'])
def delete(reservation_id):
    return reservation_delete(reservation_id)

@reservation_detail_bp.route('/not-found', methods=['GET'])
def not_found():
    return reservation_not_found()