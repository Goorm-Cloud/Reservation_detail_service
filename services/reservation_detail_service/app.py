from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy import MetaData
import os

# DB 설정
naming_convention = {
    "ix": 'ix_%(column_0_label)s',
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(column_0_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}
db = SQLAlchemy(metadata=MetaData(naming_convention=naming_convention))
migrate = Migrate()

# 모델 정의
class User(db.Model):
    __tablename__ = "user"
    user_id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    name = db.Column(db.String(20), nullable=False)
    gender = db.Column(db.String(10), nullable=False)
    email = db.Column(db.String(50), nullable=False, unique=True)  
    age = db.Column(db.Integer, nullable=False)
    phone = db.Column(db.String(20), nullable=True)
    role = db.Column(db.String(5), nullable=False)

    reservations = db.relationship("Reservation", backref="user", lazy=True)

class ParkingLot(db.Model):
    __tablename__ = "parkinglot"
    
    parkinglot_id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    parkinglot_name = db.Column(db.String(50), nullable=False)
    latitude = db.Column(db.String(20), nullable=False) 
    longitude = db.Column(db.String(20), nullable=False)
    parkinglot_div = db.Column(db.String(7), nullable=False)
    parkinglot_type = db.Column(db.String(8), nullable=True)
    parkinglot_num = db.Column(db.Integer, nullable=True)
    parkinglot_cost = db.Column(db.Boolean, nullable=True)
    parkinglot_add = db.Column(db.String(100), nullable=True) 
    parkinglot_day = db.Column(db.String(3), nullable=True)
    parkinglot_time = db.Column(db.Time, nullable=True) 

    reservations = db.relationship("Reservation", backref="parkinglot", lazy=True)

class Reservation(db.Model):
    __tablename__ = "reservation"
    
    reservation_id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    parkinglot_id = db.Column(db.Integer, db.ForeignKey("parkinglot.parkinglot_id"), nullable=False) 
    user_id = db.Column(db.Integer, db.ForeignKey("user.user_id"), nullable=False) 
    reservation_status = db.Column(db.String(7), nullable=True)
    is_deleted = db.Column(db.Boolean, default=False, nullable=False)
    
    created_at = db.Column(db.DateTime, nullable=True)
    created_by = db.Column(db.String(16), nullable=True) 
    modified_at = db.Column(db.DateTime, nullable=True)
    modified_by = db.Column(db.String(16), nullable=True)

# 애플리케이션 생성
def create_app():
    app = Flask(__name__)
    
    # 설정
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URI', 'sqlite:///reservation_detail.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.secret_key = os.getenv('SECRET_KEY', os.urandom(24))
    
    # DB 초기화
    db.init_app(app)
    migrate.init_app(app, db)
    
    # 블루프린트 등록
    from routes import reservation_detail_bp
    app.register_blueprint(reservation_detail_bp)
    
    return app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')