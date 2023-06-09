import os


class BaseConfig(object):
    DEBUG = True
    TESTING = False
    SQLALCHEMY_DATABASE_URI = "sqlite:///blog.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = "abcdefg123456"
    FLASK_ADMIN_SWATCH = "cosmo"
    OPENAPI_URL_PREFIX = "/api/swagger"
    OPENAPI_SWAGGER_UI_PATH = "/"
    OPENAPI_SWAGGER_UI_VERSION = "3.22.0"
    API_URL = "https://127.0.0.1:8000"


class DevConfig(BaseConfig):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get("SQLALCHEMY_DATABASE_URI")


class ProdConfig(BaseConfig):
    DEBUG = False
    API_URL = "https://flask-blog-rqp4.onrender.com"


class TestingConfig(BaseConfig):
    TESTING = True
