from flask import Blueprint, url_for, request, render_template, g, flash
from werkzeug.utils import redirect
from services.reservation_detail_service import db
from services.common.models import Reservation, User, ParkingLot

bp = Blueprint('reservation_detail', __name__, url_prefix='/reservation')

@bp.route('/detail/<int:reservation_id>', methods=['GET'])
def detail(reservation_id):
    reservation = Reservation.query.get_or_404(reservation_id)
    user = User.query.get_or_404(reservation.user_id)
    parkingLot = ParkingLot.query.get_or_404(reservation.parkinglot_id)
    
    return render_template('admin_reservation_detail.html', reservation=reservation, user=user,
            parkingLot=parkingLot)

@bp.route('/detail/<int:reservation_id>', methods=['POST'])
def modify(reservation_id):
    reservation = Reservation.query.get_or_404(reservation_id)

    return render_template('reservation_modify.html', reservation=reservation)