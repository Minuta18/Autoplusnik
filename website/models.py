# Autoplusnik Copyright (C) 2023 Igor Samsonov

from .app_init import db
from flask_login import UserMixin
import enum

class Permissions(enum.Enum):
    no_permissions = 0
    default_account = 1
    admin_account = 2
    dev_account = 3

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    role = db.Column(db.SmallInteger, default=Permissions.admin_account.value)
    password = db.Column(db.String(100)) #

    def __repr__(self):
        return '<User %r>' % (self.nickname)
    
class Klass(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    stepik_id = db.Column(db.Integer)
    sheet_name = db.Column(db.String(64))
    creator_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return f'<Klass ({self.name}, {self.stepik_id}, {self.sheet_name})>'