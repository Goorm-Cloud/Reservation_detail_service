from flask import Flask, render_template
from services.common.models import db, migrate
from services.reservation_detail_service.views import reservation_detail_view
import config

def create_app():
    app = Flask(__name__, template_folder="services/reservation_detail_service/templates")
    app.config.from_object(config)

    #ORM
    db.init_app(app)
    if app.config['SQLALCHEMY_DATABASE_URI'].startswith("sqlite"):
        migrate.init_app(app, db, render_as_batch=True)
    else:
        migrate.init_app(app, db)
            

    app.register_blueprint(reservation_detail_view.bp)

    return app

def page_not_found(e):
    return render_template('404.html'), 404