from flask import render_template, request, redirect, session, jsonify # type: ignore
from app import app # type: ignore
from db import db # type: ignore
from models import User, Restaurant,Review# type: ignore

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
        role = 1  # Defaults to 1, and can be set by the administrator.
        
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
            return redirect('/restaurants')
        else:
            return 'Invalid username or password, please try again.', 401

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect('/')

@app.route('/restaurants')
def restaurants():
    restaurant_list = Restaurant.query.all()  
    restaurants = [
        {
            "restaurant_id": restaurant.restaurant_id, 
            "name": restaurant.name,
            "lat": restaurant.latitude,
            "lon": restaurant.longitude,
            "info": f"{restaurant.description}<br>{restaurant.address}<br>opening hours:{restaurant.opening_hours}"
        } for restaurant in restaurant_list
    ]
    return render_template('restaurants.html', restaurants=restaurants)

@app.route('/restaurant/<int:restaurant_id>')
def restaurant_detail(restaurant_id):

    restaurant = Restaurant.query.get(restaurant_id)
    if not restaurant:
        return "Restaurant not found", 404
    
    reviews = Review.query.filter_by(restaurant_id=restaurant_id).all()
    return render_template('restaurant_detail.html', restaurant=restaurant, reviews=reviews)
