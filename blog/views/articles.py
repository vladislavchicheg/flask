from typing import Dict

import requests
from flask import Blueprint, current_app, redirect, render_template, request, url_for
from flask_login import current_user, login_required
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import joinedload
from werkzeug.exceptions import NotFound

from blog.configs import BaseConfig
from blog.extension import db
from blog.forms.article import CreateArticleForm
from blog.models import Article, Author, Tag

article_app = Blueprint("article_app", __name__, url_prefix="/articles", static_folder="../static")


@article_app.route("/")
def article_list():
    articles = Article.query.all()
    count_articles: Dict = requests.get("https://flask-blog-rqp4.onrender.com/api/articles/event_get_count/").json()
    return render_template(
        "articles/list.html", articles=articles, count_articles=count_articles["count"], active="articles"
    )


@article_app.route("/<int:pk>")
def get_article(pk: int):
    _article = Article.query.filter_by(id=pk).options(joinedload(Article.tags)).one_or_none()
    if _article is None:
        raise NotFound
    return render_template("articles/detail.html", article=_article, active="articles")


@article_app.route("/create/", methods=["GET", "POST"])
@login_required
def create_article():
    error = None
    form = CreateArticleForm(request.form)
    form.tags.choices = [(tag.id, tag.name) for tag in Tag.query.order_by("name")]
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
        if form.tags.data:
            selected_tags = Tag.query.filter(Tag.id.in_(form.tags.data))
            for tag in selected_tags:
                _article.tags.append(tag)
        db.session.add(_article)
        db.session.commit()
        return redirect(url_for("article_app.get_article", pk=_article.id))
    return render_template("articles/create.html", form=form, error=error)
