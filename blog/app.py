import os

from flask import Blueprint, Flask
from flask_combo_jsonapi import Api
from flask_login import LoginManager, login_manager

from blog import commands
from blog.views.admin import admin_app
from blog.views.articles import article_app
from blog.views.auth import auth
from blog.views.authors import authors_app
from blog.views.index import index
from blog.views.users import users_app

from .api.article import ArticleDetail, ArticleList
from .api.author import AuthorDetail, AuthorList
from .api.user import UserDetail, UserList
from .extension import (
    admin,
    create_api_event_plugin,
    create_api_spec_plugin,
    create_permission_plugin,
    csrf,
    db,
    login_manager,
    migrate,
)
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
    admin.init_app(app)
    register_api(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))


def register_api(app: Flask):

    from blog.api.tag import TagDetail, TagList

    api_blueprint = Blueprint("api", __name__)
    csrf.exempt(api_blueprint)
    api = Api(app=app, plugins=[create_api_event_plugin(app), create_api_spec_plugin(app), create_permission_plugin()])

    api.route(TagList, "tag_list", "/api/tags/")
    api.route(TagDetail, "tag_detail", "/api/tags/<int:id>")
    api.route(UserList, "user_list", "/api/users/", tag="User")
    api.route(UserDetail, "user_detail", "/api/users/<int:id>/", tag="User")
    api.route(AuthorList, "author_list", "/api/authors/", tag="Author")
    api.route(AuthorDetail, "author_detail", "/api/authors/<int:id>/", tag="Author")
    api.route(ArticleList, "article_list", "/api/articles/", tag="Article")
    api.route(ArticleDetail, "article_detail", "/api/articles/<int:id>/", tag="Article")


def register_blueprints(app: Flask):
    from blog import admin

    app.register_blueprint(index, url_prefix="/")
    app.register_blueprint(users_app, url_prefix="/users")
    app.register_blueprint(article_app, url_prefix="/articles")
    app.register_blueprint(auth, url_prefix="/auth")
    app.register_blueprint(authors_app, url_prefix="/authors")
    app.register_blueprint(admin_app, url_prefix="/admin")
    admin.register_views()


def register_commands(app: Flask):
    app.cli.add_command(commands.create_init_user)
    app.cli.add_command(commands.create_tags)
