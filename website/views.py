# Autoplusnik Copyright (C) 2023 Igor Samsonov

from . import models
from .app_init import db
from .app_init import app
from ConfigParser import Config
from werkzeug.security import generate_password_hash, check_password_hash
from flask import render_template, request, redirect, abort
from flask_login import login_user
from .models import User, Klass
from .permissions import Permissions, role_to_text, is_current_user_admin
from flask_login import login_required, current_user, logout_user
from Plusnik import add_task, UpdateTask, task_queue

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html', usr=current_user, is_admin=is_current_user_admin())

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

                return redirect('/klasses/')

    return render_template(
        'edit.html', 
        old_name=klass.name,
        old_id=klass.stepik_id,
        old_sheet=klass.sheet_name, 
        is_admin=(is_current_user_admin()),   
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
@login_required
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
            elif action == 'update':
                tklass = Klass.query.filter_by(id=int(klass)).first()

                if tklass == None:
                    abort(404)

                if current_user.id != tklass.creator_id:
                    abort(403)

                add_task(
                    tklass.id,
                    tklass.stepik_id,
                    tklass.sheet_name,
                )

    all_klasses = Klass.query.filter_by(creator_id=current_user.id)

    return render_template(
        'klasses.html', 
        klasses=all_klasses, 
        all_len=all_klasses.count(), 
        usr=current_user, 
        is_admin=is_current_user_admin(),
    )

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
        
        user = User.query.filter_by(username=username).first()
        if user:
            return render_template('register.html', alerts="Имя пользователя уже занято")

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

@app.route('/admin/', methods=['GET', 'POST'])
@login_required
def admin_panel(): #TODO: clean this code up
    if current_user.role != Permissions.admin_account.value and \
       current_user.role != Permissions.dev_account.value:
        abort(403)

    action = request.args.get('action')
    user_id = request.args.get('user_id')

    if action != None and user_id != None:
        try:
            user_id = int(user_id)
        except: # TODO: add exception
            abort(400)
        
        editable_user = User.query.filter_by(id=user_id).first()

        if editable_user.role ==  Permissions.dev_account.value and \
           current_user.role != Permissions.dev_account.value:
            abort(403)

        if action == 'ban': # TODO: optimize
            if current_user.id == user_id:
                return redirect('/admin/')

            usr_klasses = Klass.query.filter_by(creator_id=user_id).all()
            for klass in usr_klasses:
                db.session.delete(klass)
            db.session.delete(editable_user)
            db.session.commit()
        elif action == 'edit':
            user = User.query.filter_by(id=user_id).first()
            user.role = request.form.get('role')
            print(user.role)
            db.session.commit()
        else:
            abort(403)

        return redirect('/admin/')

    users = User.query.all()
    return render_template('admin.html', selected_users=users, is_dev=(current_user.role == Permissions.dev_account.value), role_to_text=role_to_text)

@app.route('/logout/', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()

    return redirect('/')

# TODO: remove duplication
@app.errorhandler(404)
def error404(err):
    return render_template('error.html', usr=current_user, error_code=404, is_admin=is_current_user_admin(),), 404

@app.errorhandler(400)
def error400(err):
    return render_template('error.html', usr=current_user, error_code=400, is_admin=is_current_user_admin(),), 400

@app.errorhandler(500)
def error500(err):
    return render_template('error.html', usr=current_user, error_code=500, is_admin=is_current_user_admin(),), 500

@app.errorhandler(403)
def error403(err):
    return render_template('error.html', usr=current_user, error_code=403, is_admin=is_current_user_admin(),), 403