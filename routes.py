from flask import render_template, request, redirect, session
from app import app
from db import db
from models import User

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    elif request.method == 'POST':
        name = request.form['name']
        password = request.form['password']
        role = 1  # 你可以根据需要设置角色，暂时设为1
        
        if User.query.filter_by(name=name).first():
            return 'Username already exists', 400
        
        new_user = User(name=name, role=role)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()

        return redirect('/login')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    elif request.method == 'POST':
        name = request.form['name']
        password = request.form['password']
        
        user = User.query.filter_by(name=name).first()
        if user and user.check_password(password):
            session['username'] = user.name
            return 'Login successful', 200
        else:
            return 'Invalid username or password, please try again.', 401

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect('/')
