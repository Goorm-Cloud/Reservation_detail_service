# config
import os
DEBUG = False

# DB 모드 설정 (sqlite 또는 mysql)
DB_MODE = os.getenv('DB_MODE', 'mysql')

# DB 관련 설정
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# SQLite 설정
DB_PATH = os.path.join(BASE_DIR, "services/common/parking.db")
SQLITE_URI = f"sqlite:///{DB_PATH}"

# MySQL 설정
MYSQL_USER = os.getenv('MYSQL_USER', 'zochacha')
MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD', 'password')
MYSQL_HOST = os.getenv('MYSQL_HOST', 'mysql')
MYSQL_PORT = os.getenv('MYSQL_PORT', '3306')
MYSQL_DB = os.getenv('MYSQL_DB', 'zochacha')
MYSQL_URI = f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DB}"

# 사용할 DB URI 설정
if DB_MODE == 'mysql':
    SQLALCHEMY_DATABASE_URI = MYSQL_URI
else:
    SQLALCHEMY_DATABASE_URI = SQLITE_URI

SQLALCHEMY_TRACK_MODIFICATIONS = False

# URL_Prefix
ADMIN_SERVICE_URL = '/admin'
MAP_SERVICE_URL = '/map'
RESERVATION_SERVICE_URL = '/reservation'
PARKINGLOT_SERVICE_URL = '/parking-lot'
RESERVATION_DETAIL_SERVICE_URL = '/reservation-detail' 