from flask import render_template, request
from services.common.models import db, Reservation, User

def admin_dashboard():
    page = request.args.get("page", 1, type=int)  # 현재 페이지 번호 (기본값: 1)
    per_page = 10  # 한 페이지에 표시할 데이터 개수
    reservations = Reservation.query.paginate(page=page, per_page=per_page, error_out=False)

    return render_template('admin_list.html', reservations=reservations)
