from sqlalchemy import Column, ForeignKey, Integer, Table

from blog.extension import db

article_tag_association_table = Table(
    "article_tag_association",
    db.metadata,
    Column("article_id", Integer, ForeignKey("articles.id"), nullable=False),
    Column("tag_id", Integer, ForeignKey("tag.id"), nullable=False),
)
