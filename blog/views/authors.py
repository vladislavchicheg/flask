import requests
from flask import Blueprint, render_template

from blog.models import Author

authors_app = Blueprint("authors_app", __name__, url_prefix="/authors", static_folder="../static")


@authors_app.route("/")
def authors_list():
    authors = Author.query.all()
    article_count = {}
    for author in authors:
        article_count[author.id] = requests.get(
            f"http://127.0.0.1:5000/api/authors/{author.id}/event_get_articles_count/"
        ).json()
    return render_template("authors/list.html", article_count=article_count, authors=authors)
