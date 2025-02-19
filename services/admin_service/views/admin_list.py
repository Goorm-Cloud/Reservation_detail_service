from flask import render_template
from ..models import reservations

def admin_dashboard():
    return render_template('admin_list.html', reservations=reservations)
