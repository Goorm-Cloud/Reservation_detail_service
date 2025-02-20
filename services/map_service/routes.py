from flask import Blueprint, render_template, request, redirect, url_for
from .views.map_view import home_view, static_files, get_parking_lots

map_bp = Blueprint("map_bp", __name__)

# 📌 URL과 뷰 연결
map_bp.route("/", endpoint="index")(home_view)
map_bp.route("/static/<path:filename>")(static_files)
map_bp.route("/api/parking-lots")(get_parking_lots)


# 📌 `/map`에서 주차장을 클릭하면 상세 페이지로 이동
@map_bp.route("/map/<int:parkinglot_id>", methods=["GET"])
def parking_lot_redirect(parkinglot_id):

    return redirect(url_for("parkinglot_bp.parking_lot_detail_route", parkinglot_id=parkinglot_id))