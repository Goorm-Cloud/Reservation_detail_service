from flask import Blueprint
from .views.map_view import home_view, static_files, get_parking_lots

map_bp = Blueprint("map_bp", __name__)

# 📌 URL과 뷰 연결
map_bp.route("/", endpoint="index")(home_view)
map_bp.route("/static/<path:filename>")(static_files)
map_bp.route("/api/parking-lots")(get_parking_lots)
