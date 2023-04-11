from flask import Blueprint, current_app, redirect, render_template, request, url_for
from flask_login import current_user, login_user
from sqlalchemy.exc import IntegrityError
from werkzeug.exceptions import NotFound
from werkzeug.security import generate_password_hash

from blog.extension import db
from blog.forms.user import UserRegisterForm
from blog.models import User

users_app = Blueprint("users_app", __name__, url_prefix="/users", static_folder="../static")


@users_app.route("/")
def users_list():
    users = User.query.all()
    return render_template("users/list.html", users=users)


@users_app.route("/<int:user_id>/")
def user_details(user_id: int):
    user = User.query.filter_by(id=user_id).one_or_none()
    if user is None:
        raise NotFound(f"User #{user_id} doesn't exist!")
    return render_template("users/detail.html", user=user)


@users_app.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("users_app.user_details", user_id=current_user.id))

    form = UserRegisterForm(request.form)
    errors = []

    if form.validate_on_submit():
        if User.query.filter_by(email=form.email.data).count():
            form.email.errors.append("email already exists")
            return render_template("users/register.html", form=form)

        user = User(
            email=form.email.data,
            username=form.email.data,
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            password=generate_password_hash(form.password.data),
            is_staff=False,
        )

        db.session.add(user)
        try:
            db.session.commit()
        except IntegrityError:
            current_app.logger.exception("Could not create user!")
            form.email.errors.append("Could not create user!")
        else:
            current_app.logger.info("Created user %s", user)
            login_user(user)
            return redirect(url_for("users_app.user_details", user_id=current_user.id))

    return render_template(
        "users/register.html",
        form=form,
        errors=errors,
    )
