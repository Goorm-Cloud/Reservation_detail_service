import os

from flask import Flask, url_for
from services.common.models import db, migrate
from services.common.oauth import oauth

from services.reservation_detail_service.routes import reservation_detail_bp


def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('config.py')
    app.secret_key = os.urandom(24)


    # 📌 OAuth 설정
    oauth.init_app(app)
    oauth.register(
        name='oidc',
        authority='https://cognito-idp.ap-northeast-2.amazonaws.com/ap-northeast-2_HroMsatHG',
        client_id='77g5eu474omofv1t6ss848gn9u',
        client_secret= os.getenv("CLIENT_SECRET"),
        server_metadata_url='https://cognito-idp.ap-northeast-2.amazonaws.com/ap-northeast-2_HroMsatHG/.well-known/openid-configuration',
        client_kwargs={'scope': 'phone openid email'}
    )


    # 📌 템플릿 자동 리로드 설정
    app.config['TEMPLATES_AUTO_RELOAD'] = True


    # 📌 DB 설정
    db.init_app(app)
    migrate.init_app(app, db)


    @app.route("/")
    def index():
        from flask import redirect
        return redirect(url_for("reservation_detail_bp.detail", reservation_id=1))  # 예약 상세 페이지로 리디렉트

    # 📌 블루프린트 등록
    app.register_blueprint(reservation_detail_bp, url_prefix=app.config['RESERVATION_DETAIL_SERVICE_URL'])


    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
