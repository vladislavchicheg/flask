from flask import Flask
from flask_login import LoginManager, login_manager

from blog.models.database import db
from blog.views.articles import article
from blog.views.auth import auth
from blog.views.index import index
from blog.views.users import users_app

from .extension import login_manager


def create_app() -> Flask:
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "sdflkjsd5k4sdfsdf423kao9!ds#=dssd"
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///blog.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)

    login_manager.login_view = "auth.login"
    login_manager.init_app(app)
    register_blueprints(app)
    return app


def register_blueprints(app: Flask):
    app.register_blueprint(index, url_prefix="/")
    app.register_blueprint(users_app, url_prefix="/users")
    app.register_blueprint(article, url_prefix="/articles")
    app.register_blueprint(auth, url_prefix="/auth")
