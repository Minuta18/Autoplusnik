from . import models
from .app_init import db
from .app_init import app
from ConfigParser import Config
from werkzeug.security import generate_password_hash, check_password_hash
from flask import Flask, render_template, request, redirect
from flask_login import login_user
from .models import User
from flask_login import login_required, current_user, logout_user

@app.route('/', methods=['GET', 'POST'])
def index():
    # if request.method == 'POST':
    #     action = request.args.get('action')
    #     klass = request.args.get('klass')

    #     if action != None and klass != None:
    #         if action == 'update':
    #             pass # TODO
    #         elif action == 'delete':
    #             pass
    #         elif action == 'create':
    #             pass
    #         elif action == 'edit':
    #             pass
        
    #     return redirect('/')
    # return render_template(...) # TODO
    return render_template('index.html', usr=current_user)

@app.route('/login/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = User.query.filter_by(username=username).first()

        if not user or not check_password_hash(user.password, password):
            return render_template('login.html', alert='Логин или пароль не совпадают')
        
        login_user(user)
        return redirect('/')

    return render_template('login.html', alert='')

@app.route('/register/', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        password2 = request.form.get('confirm_password')
        if password != password2:
            return render_template('register.html', alerts="Пароли не совпадают")
        user = User.query.filter_by(email=email).first()
        if user:
            return render_template('register.html', alerts="Почта уже занята")
        
        new_user = User(
            email=email,
            username=username,
            password=generate_password_hash(password, method='sha256')
        )

        db.session.add(new_user)
        db.session.commit()
        
        login_user(new_user)

        return redirect('/')
    return render_template('register.html', alerts='')

@app.route('/logout/', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()

    return redirect('/')

@app.route('/edit/', methods=['GET', 'POST'])
@login_required
def edit():
    # TODO
    return render_template('edit.html')