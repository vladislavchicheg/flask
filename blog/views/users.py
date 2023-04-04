from flask import Blueprint, render_template
from werkzeug.exceptions import NotFound

user = Blueprint("user", __name__, url_prefix="/users", static_folder="../static")

USERS = {
    1: "Petya",
    2: "Kolya",
    3: "Olya",
    4: "Volodya",
}


@user.route("/")
def user_list():
    return render_template("users/list.html", users=USERS, active="users")


@user.route("/<int:pk>")
def get_user(pk: int):
    try:
        user = USERS[pk]
    except KeyError:
        raise NotFound(f"User id {pk} not found")
    return render_template("users/detail.html", user_name=user, active="users")
