from combojsonapi.event import EventPlugin
from combojsonapi.permission import PermissionPlugin
from combojsonapi.spec import ApiSpecPlugin
from flask_admin import Admin
from flask_combo_jsonapi import Api
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import CSRFProtect

from blog.views.admin import CustomAdminIndexView


def create_api_spec_plugin(app):
    api_spec_plugin = ApiSpecPlugin(
        app=app,
        # Declaring tags list with their descriptions,
        # so API gets organized into groups. it's optional.
        tags={
            "Tag": "Tag API",
            "User": "User API",
            "Author": "Author API",
            "Article": "Article API",
        },
    )
    return api_spec_plugin


def create_api_event_plugin(app):
    api_event_plugin = EventPlugin()

    return api_event_plugin


def create_permission_plugin():
    return PermissionPlugin()


db = SQLAlchemy()
login_manager = LoginManager()
migrate = Migrate()
csrf = CSRFProtect()
admin = Admin(index_view=CustomAdminIndexView(), name="Blog Admin Panel", template_mode="bootstrap4")
