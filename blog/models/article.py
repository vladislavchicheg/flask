from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String, Text, func
from sqlalchemy.orm import relationship

from blog.extension import db
from blog.models.article_tag import article_tag_association_table


class Article(db.Model):
    __tablename__ = "articles"
    id = db.Column(db.Integer, primary_key=True)
    author_id = db.Column(db.Integer, ForeignKey("authors.id"), nullable=False)
    title = db.Column(db.String(200), nullable=False, default="", server_default="")
    body = db.Column(db.Text, nullable=False, default="", server_default="")
    dt_created = db.Column(db.DateTime, default=datetime.utcnow, server_default=func.now())
    dt_updated = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    author = relationship("Author", back_populates="articles")
    tags = relationship(
        "Tag",
        secondary=article_tag_association_table,
        back_populates="articles",
    )

    def __str__(self):
        return self.title
