# Autoplusnik Copyright (C) 2023 Igor Samsonov

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from . import config
from flask_login import LoginManager

app = Flask(__name__)
app.config.from_object(config)
db = SQLAlchemy(app)


login_manager = LoginManager()
login_manager.login_view = 'views.login'
login_manager.init_app(app)