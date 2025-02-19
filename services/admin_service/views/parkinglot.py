from flask import render_template, redirect, url_for, request
from ..models import parkinglots

def edit_parkinglot(parkinglot_id):
    parkinglot = next((p for p in parkinglots if p["id"] == parkinglot_id), None)
    if not parkinglot:
        return "주차장을 찾을 수 없습니다.", 404

    if request.method == 'POST':
        parkinglot["name"] = request.form['name']
        parkinglot["latitude"] = request.form['latitude']
        parkinglot["longitude"] = request.form['longitude']
        parkinglot["type"] = request.form['type']
        parkinglot["capacity"] = request.form['capacity']
        parkinglot["fee"] = request.form['fee']
        parkinglot["hours"] = request.form['hours']

       # return redirect(url_for('admin.admin_dashboard')) # 추후 수정

    return render_template('edit_parkinglot.html', parkinglot=parkinglot)