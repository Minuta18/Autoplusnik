# Autoplusnik Copyright (C) 2023 Igor Samsonov

from flask import Flask, redirect, render_template, request
from flask_sqlalchemy import SQLAlchemy
from . import config
from flask_login import LoginManager
from . import views
from .app_init import app
from .app_init import db
from .app_init import login_manager
from .models import User

with app.app_context():
    db.create_all()  

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id) #