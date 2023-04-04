from flask import Flask

from blog.views.articles import article
from blog.views.users import user


def create_app() -> Flask:
    app = Flask(__name__)
    register_blueprints(app)
    return app


def register_blueprints(app: Flask):
    app.register_blueprint(user, url_prefix="/users")
    app.register_blueprint(article, url_prefix="/articles")
