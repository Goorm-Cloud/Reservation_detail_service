import os

from flask import Flask
from authlib.integrations.flask_client import OAuth
from services.admin_service.routes import admin_bp, login_bp
from services.map_service.routes import map_bp
from services.reservation_service.routes import parkinglot_bp
from services.reservation_service.reservation_route import reservation_bp
from services.common.models import db, migrate
from flask_migrate import Migrate

# from services.reservation_detail_service.routes import reservation_detail_bp
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv


def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('config.py')
   # load_dotenv(ENV_PATH)

    # 📌 OAuth 설정
    oauth = OAuth(app)
    app.config['CLIENT_SECRET'] = os.getenv("CLIENT_SECRET")
    oauth.register(
        name='oidc',
        authority='https://cognito-idp.ap-northeast-2.amazonaws.com/ap-northeast-2_HroMsatHG',
        client_id='77g5eu474omofv1t6ss848gn9u',
        client_secret= app.config['CLIENT_SECRET'],
        server_metadata_url='https://cognito-idp.ap-northeast-2.amazonaws.com/ap-northeast-2_HroMsatHG/.well-known/openid-configuration',
        client_kwargs={'scope': 'phone openid email'}
    )


    # 📌 KAKAO API KEY 로드
    app.config['KAKAO_API_KEY'] = os.getenv("KAKAO_API_KEY")
    if not app.config['KAKAO_API_KEY']:
        raise ValueError("❌ KAKAO_API_KEY가 설정되지 않았습니다! .env 파일을 확인하세요.")
    app.config['TEMPLATES_AUTO_RELOAD'] = True

    # 📌 DB 설정
    db.init_app(app)
    migrate.init_app(app, db)

    #  📌 블루프린트 등록
    app.register_blueprint(login_bp)
    app.register_blueprint(admin_bp, url_prefix=app.config['ADMIN_SERVICE_URL'])
    app.register_blueprint(map_bp, url_prefix=app.config['MAP_SERVICE_URL'])
    app.register_blueprint(reservation_bp, url_prefix=app.config['RESERVATION_SERVICE_URL'])
    app.register_blueprint(parkinglot_bp, url_prefix=app.config['PARKINGLOT_SERVICE_URL'])

    # app.register_blueprint(reservation_detail_bp, url_prefix=app.config['RESERVATION_DETAIL_SERVICE_URL'])

    return app
