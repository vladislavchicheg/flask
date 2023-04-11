import os

from flask import Flask
from flask_login import LoginManager, login_manager
from flask_migrate import Migrate

from blog import commands
from blog.views.articles import article
from blog.views.auth import auth
from blog.views.index import index
from blog.views.users import users_app

from .extension import db, login_manager, migrate
from .models import User


def create_app() -> Flask:
    app = Flask(__name__)
    cfg_name = os.environ.get("CONFIG_NAME") or "BaseConfig"
    app.config.from_object(f"blog.configs.{cfg_name}")

    registr_extensions(app)
    register_blueprints(app)
    register_commands(app)
    return app


@login_manager.user_loader
def load_user(user):
    return User.get(user)


def registr_extensions(app):
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.login_view = "auth.login"
    login_manager.init_app(app)


def register_blueprints(app: Flask):
    app.register_blueprint(index, url_prefix="/")
    app.register_blueprint(users_app, url_prefix="/users")
    app.register_blueprint(article, url_prefix="/articles")
    app.register_blueprint(auth, url_prefix="/auth")


def register_commands(app: Flask):
    app.cli.add_command(commands.create_init_user)
