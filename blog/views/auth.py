from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required, login_user, logout_user
from werkzeug.security import check_password_hash, generate_password_hash

from blog.extension import db
from blog.forms.user import LoginForm, UserRegisterForm
from blog.models import User

auth = Blueprint("auth", __name__, static_folder="../static")


@auth.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("users_app.user_details", user_id=current_user.id))

    form = LoginForm(request.form)
    errors = []
    if request.method == "POST" and form.validate():
        email = request.form.get("email")
        password = request.form.get("password")
        user = User.query.filter_by(email=email).first()
        if not user or not check_password_hash(user.password, password):
            flash("Check your login details")
            return redirect(url_for(".login"))
        login_user(user)
        return redirect(url_for("users_app.user_details", user_id=user.id))
    return render_template(
        "auth/login.html",
        form=form,
        errors=errors,
    )


@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for(".login"))
