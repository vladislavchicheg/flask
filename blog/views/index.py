from flask import Blueprint, render_template
from werkzeug.exceptions import NotFound

index = Blueprint("index_page", __name__, url_prefix="/", static_folder="../static")


@index.route("/")
def index_page():
    return render_template("index.html")
