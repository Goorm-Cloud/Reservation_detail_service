from flask import render_template, redirect, url_for, session
from services.common.oauth import oauth
from flask import current_app

def login():
    return oauth.oidc.authorize_redirect(current_app.config['AUTHORIZE_REDIRECT_URL'])


def logout():
    session.pop('user', None)
    return redirect(url_for('index')) #민승님 메인 화면으로 이동


def role_check():
    user = session.get('user')
    user_groups = user.get('cognito:groups', [])

    if "admin" in user_groups:
        return redirect(url_for('admin_bp.admin_dashboard_route'))
    elif "user" in user_groups:
        #return redirect(url_for('민승님 메인 라우트 연결 예정'))
        return f'Hello, {user.get("email")}. 당신은 유저<a href="/logout">Logout</a>'
    else:
        return f'Hello, {user.get("email")}. 당신은 알 수 없는 역할.<a href="/logout">Logout</a>'


def authorize():
    token = oauth.oidc.authorize_access_token()
    print("토큰 정보: ", token)
    user = token['userinfo']
    session['user'] = user

    return role_check()


