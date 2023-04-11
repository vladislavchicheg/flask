import click
from werkzeug.security import generate_password_hash

from blog.extension import db


@click.command("create-init-user")
def create_init_user():
    from blog.models import User
    from wsgi import app

    with app.app_context():
        db.session.add(
            User(
                email="admin@blog.ru",
                password=generate_password_hash("123"),
                first_name="Admin",
                last_name="Adminov",
                username="admin",
                is_staff=True,
            )
        )
        db.session.commit()
