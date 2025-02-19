from flask import render_template, redirect, url_for, request
from ..models import reservations

def add_reservation():
    if request.method == 'POST':
        new_reservation = {
            "id": len(reservations) + 1,
            "name": request.form['name'],
            "car_number": request.form['car_number'],
            "date": request.form['date'],
            "time": request.form['time'],
        }
        reservations.append(new_reservation)
        return redirect(url_for('admin.admin_dashboard'))
    return render_template('add_reservation.html')

def edit_reservation(reservation_id):
    reservation = next((r for r in reservations if r["id"] == reservation_id), None)
    if not reservation:
        return "예약을 찾을 수 없습니다.", 404

    if request.method == 'POST':
        reservation["name"] = request.form['name']
        reservation["car_number"] = request.form['car_number']
        reservation["date"] = request.form['date']
        reservation["time"] = request.form['time']
        return redirect(url_for('admin.admin_dashboard'))

    return render_template('edit_reservation.html', reservation=reservation)

def delete_reservation(reservation_id):
    reservation = next((r for r in reservations if r["id"] == reservation_id), None)
    if not reservation:
        return "예약을 찾을 수 없습니다.", 404

    if request.method == 'POST':
        reservations.remove(reservation)
        return redirect(url_for('admin_dashboard'))

    return render_template('delete_reservation.html', reservation=reservation)

def reservation_detail(reservation_id):
    # reservation_id에 해당하는 예약을 찾음
    reservation = next((r for r in reservations if r['id'] == reservation_id), None)

    if reservation is None:
        return "예약을 찾을 수 없습니다.", 404

    return render_template('reservation_detail.html', reservation=reservation)
