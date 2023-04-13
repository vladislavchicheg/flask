import os

from flask import Flask
from flask_login import LoginManager, login_manager
from flask_migrate import Migrate

from blog import commands
from blog.views.articles import article
from blog.views.auth import auth
from blog.views.authors import authors_app
from blog.views.index import index
from blog.views.users import users_app

from .extension import csrf, db, login_manager, migrate
from .models import Author, User


def create_app() -> Flask:
    app = Flask(__name__)
    cfg_name = os.environ.get("CONFIG_NAME") or "BaseConfig"
    app.config.from_object(f"blog.configs.{cfg_name}")

    registr_extensions(app)
    register_blueprints(app)
    register_commands(app)
    return app


def registr_extensions(app):
    db.init_app(app)
    migrate.init_app(app, db)
    csrf.init_app(app)
    login_manager.login_view = "auth.login"
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))


def register_blueprints(app: Flask):
    app.register_blueprint(index, url_prefix="/")
    app.register_blueprint(users_app, url_prefix="/users")
    app.register_blueprint(article, url_prefix="/articles")
    app.register_blueprint(auth, url_prefix="/auth")
    app.register_blueprint(authors_app, url_prefix="/authors")


def register_commands(app: Flask):
    app.cli.add_command(commands.create_init_user)
