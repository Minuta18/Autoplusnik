# Autoplusnik Copyright (C) 2023 Igor Samsonov

from . import models
from .app_init import db
from .app_init import app
from ConfigParser import Config
from werkzeug.security import generate_password_hash, check_password_hash
from flask import Flask, render_template, request, redirect, abort
from flask_login import login_user
from .models import User, Klass, Permissions
from flask_login import login_required, current_user, logout_user

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html', usr=current_user)

@login_required
@app.route('/edit/<klass_id>', methods=['GET', 'POST'])
def edit(klass_id: int):
    if current_user.role == Permissions.no_permissions.value:
        abort(403)

    klass = Klass.query.filter_by(id=klass_id).first()

    if klass.creator_id != current_user.id:
        abort(403)

    if request.method == 'POST':
        form_ = int(request.args.get('form'))

        if form_ != None:
            if form_ == 0:
                klass.name = request.form.get('name_')
                klass.stepik_id = int(request.form.get('klass_id'))
                klass.sheet_name = request.form.get('lname')

                db.session.commit()
            elif form_ == 1:
                ...

        return redirect('/klasses/')

    return render_template(
        'edit.html', 
        old_name=klass.name,
        old_id=klass.stepik_id,
        old_sheet=klass.sheet_name,    
    )

@login_required
@app.route('/delete/<klass_id>/', methods=['GET'])
def delete(klass_id):
    klass = Klass.query.filter_by(id=klass_id).first()

    if current_user.id == klass.creator_id:
        db.session.delete(klass)
        db.session.commit()
    else:
        abort(403)

    return redirect('/klasses/')

@login_required
@app.route('/klasses/', methods=['GET', 'POST'])
def klasses():
    if request.method == 'POST':
        klass = request.args.get('klass')
        action = request.args.get('action')

        if klass != None or action != None:
            if action == 'new':
                if current_user.role == Permissions.no_permissions.value:
                    abort(403)

                new_klass = Klass(
                    name='Новый класс',
                    stepik_id=0,
                    sheet_name='Укажите здесь лист',
                    creator_id=current_user.id, 
                )

                db.session.add(new_klass)
                db.session.commit()

                return redirect(f'/edit/{new_klass.id}')

    all_klasses = Klass.query.filter_by(creator_id=current_user.id)

    return render_template('klasses.html', klasses=all_klasses, all_len=all_klasses.count(), usr=current_user)

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