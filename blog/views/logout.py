from flask import redirect, url_for
from flask_login import login_required, logout_user


@logout.route("/logout/", endpoint="logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("index"))


@logout.route("/secret/")
@login_required
def secret_view():
    return "Super secret data"
