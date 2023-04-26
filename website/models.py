from .app_init import db
from flask_login import UserMixin
import enum

class Permissions(enum.Enum):
    default_user = 0
    admin = 1
    no_permissions = 2

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    role = db.Column(db.SmallInteger, default=Permissions.no_permissions.value)
    password = db.Column(db.String(100))

    def __repr__(self):
        return '<User %r>' % (self.nickname)