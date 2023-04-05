from sqlalchemy import Boolean, Column, Integer, String
from sqlalchemy.orm import relationship

from blog.models.database import db


class Article(db.Model):
    __tablename__ = "articles"
    id = Column(Integer, primary_key=True)
    title = Column(String(255), nullable=False)
    text = Column(String)

    def __repr__(self):
        return f"<User #{self.id} {self.title!r}>"
