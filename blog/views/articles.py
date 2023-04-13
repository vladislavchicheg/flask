from flask import Blueprint, current_app, redirect, render_template, request, url_for
from flask_login import current_user, login_required
from sqlalchemy.exc import IntegrityError
from werkzeug.exceptions import NotFound

from blog.extension import db
from blog.forms.article import CreateArticleForm
from blog.models import Article, Author

article = Blueprint("article", __name__, url_prefix="/articles", static_folder="../static")


@article.route("/")
def article_list():
    articles = Article.query.all()
    return render_template("articles/list.html", articles=articles, active="articles")


@article.route("/<int:pk>")
def get_article(pk: int):
    _article = Article.query.filter_by(id=pk).one_or_none()
    if article is None:
        raise NotFound
    return render_template("articles/detail.html", article=_article, active="articles")


@article.route("/create/", methods=["GET", "POST"])
@login_required
def create_article():
    error = None
    form = CreateArticleForm(request.form)

    if form.validate_on_submit():
        _article = Article(title=form.title.data.strip(), body=form.body.data)
        if current_user.author:
            # use existing author if present
            _article.author_id = current_user.id
        else:
            # otherwise create author record
            author = Author(user_id=current_user.id)
            _article.author_id = current_user.id
            db.session.add(author)
            db.session.flush()
        db.session.add(_article)
        db.session.commit()
        return redirect(url_for("article.get_article", pk=_article.id))
    return render_template("articles/create.html", form=form, error=error)
