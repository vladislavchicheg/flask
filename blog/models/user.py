from flask_login import UserMixin

from blog.extension import db


class User(db.Model, UserMixin):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(255))
    first_name = db.Column(db.String(255))
    last_name = db.Column(db.String(255))
    password = db.Column(db.String(255))
    is_staff = db.Column(db.Boolean, nullable=False, default=False)

    def __init__(self, email, first_name, last_name, password, username, is_staff):
        self.email = email
        self.password = password
        self.first_name = first_name
        self.last_name = last_name
        self.username = username
        self.is_staff = is_staff
