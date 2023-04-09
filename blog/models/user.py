from flask_login import UserMixin
from sqlalchemy import Boolean, Column, Integer, String

from blog.extension import login_manager
from blog.models.database import db


@login_manager.user_loader
def load_user(user):
    return User.get(user)


class User(db.Model, UserMixin):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String(80), unique=True, nullable=False)
    email = Column(String(255), unique=True)
    password = Column(String(255))
    is_staff = Column(Boolean, nullable=False, default=False)

    def __repr__(self):
        return f"<User #{self.id} {self.username!r}>"
