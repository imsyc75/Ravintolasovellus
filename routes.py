from flask import request, render_template, redirect, session # type: ignore
from app import app # type: ignore
from db import get_db_connection # type: ignore
from werkzeug.security import generate_password_hash, check_password_hash # type: ignore



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
        role = request.form['role']
        
        hashed_password = generate_password_hash(password)
                                                 
        conn = get_db_connection()
        cur = conn.cursor()

        try:
            sql = """SELECT * FROM users WHERE name = %s"""
            cur.execute(sql, (name,))
            if cur.fetchone():
                return 'Username already exists', 400
            
            sql = """INSERT INTO users (name, password, role) VALUES (%s, %s, %s)"""
            cur.execute(sql ,(name, hashed_password, role))
            conn.commit()

        except Exception as e:
            conn.rollback()
            return str(e), 500
        finally:
            cur.close()
            conn.close()

        return redirect('/login')



@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    elif request.method == 'POST':
        name = request.form.get('name')
        password = request.form.get('password')
        role = request.form.get('role')

        if not name or not password or not role:
            return "Please fill out all fields.", 400

        conn = get_db_connection()
        cur = conn.cursor()
        try:
            sql = """SELECT name, password, role FROM users WHERE name = %s"""
            cur.execute(sql, (name,))
            user = cur.fetchone()

            if user and check_password_hash(user[1], password):
                session['username'] = user[0]
                session['role'] = user[2]
                if user[2] == 0:  
                    return redirect('/admin_page')
                else:
                    return redirect('/')
            else:
                return 'Invalid username or password, please try again.', 401
        except Exception as e:
            return str(e), 500
        finally:
            cur.close()
            conn.close()



@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect('/')



@app.route('/restaurants') 
def restaurants():
    conn = get_db_connection()
    cur = conn.cursor()
    sql = """SELECT restaurant_id, name, latitude, longitude, 
            description, address, opening_hours 
            FROM restaurants"""
    cur.execute(sql)

    restaurant_list = cur.fetchall()
    restaurants = [
        {
            "restaurant_id": restaurant[0],
            "name": restaurant[1],
            "lat": restaurant[2],
            "lon": restaurant[3],
            "info": f"{restaurant[4]}<br>{restaurant[5]}<br>opening hours:{restaurant[6]}"
        } for restaurant in restaurant_list
    ]
    cur.close()
    conn.close()
    return render_template('restaurants.html', restaurants=restaurants)



@app.route('/restaurant/<int:restaurant_id>')
def restaurant_detail(restaurant_id):
    conn = get_db_connection()
    cur = conn.cursor()
    sql = """SELECT * FROM restaurants WHERE restaurant_id = %s"""
    cur.execute(sql, (restaurant_id,))
    restaurant_info = cur.fetchone()

    if not restaurant_info:
        cur.close()
        conn.close()
        return "Restaurant not found", 404
    
    restaurant = {
        "restaurant_id": restaurant_info[0],
        "name": restaurant_info[1],
        "address": restaurant_info[2],
        "description": restaurant_info[3],
        "latitude": restaurant_info[4],
        "longitude": restaurant_info[5],
        "opening_hours": restaurant_info[6]
    }
    sql = """ SELECT r.*, u.name  
              FROM reviews r JOIN users u ON r.user_id = u.id 
              WHERE r.restaurant_id = %s"""
    cur.execute(sql, (restaurant_id,))
    reviews_details = cur.fetchall()
    
    reviews = [
        {
            "review_id": review[0],
            "restaurant_id": review[1],
            "user_id": review[2],
            "rating": review[3],
            "comment": review[4],
            "timestamp": review[5],
            "user_name": review[6]
        } for review in reviews_details
    ]

    cur.close()
    conn.close()
    return render_template('restaurant_detail.html', restaurant=restaurant, reviews=reviews)



@app.route('/restaurant/<int:restaurant_id>/add_review', methods=['POST'])
def add_review(restaurant_id):
    if 'username' not in session:
        return redirect('/login')
    
    conn = get_db_connection()
    cur = conn.cursor()
    sql = """SELECT id FROM users WHERE name = %s"""
    cur.execute(sql, (session['username'],))
    user = cur.fetchone()
    if not user:
        return 'User not found', 404

    comment = request.form['comment']
    rating = float(request.form['rating'])
    sql = """INSERT INTO reviews (restaurant_id, user_id, rating, comment) VALUES (%s, %s, %s, %s)"""
    cur.execute(sql,(restaurant_id, user[0], rating, comment))
    conn.commit()
    cur.close()
    conn.close()
    return redirect(f'/restaurant/{restaurant_id}')



@app.route('/delete_review/<int:review_id>', methods=['POST'])
def delete_review(review_id):
    if 'username' not in session or session['role'] != 0:
        return "Unauthorized", 403 
    conn = get_db_connection()
    cur = conn.cursor()
    sql = "DELETE FROM reviews WHERE review_id = %s"
    cur.execute(sql, (review_id,))
    conn.commit()
    cur.close()
    conn.close()
    return redirect(request.referrer) 



@app.route('/admin_page')
def admin_page():
    conn = get_db_connection()  
    cur = conn.cursor()
    sql = "SELECT * FROM restaurants"
    cur.execute(sql)
    restaurants = cur.fetchall()
    cur.close()
    conn.close()

    return render_template('admin_page.html', restaurants=restaurants)


@app.route('/add_restaurant', methods=['GET', 'POST'])
def add_restaurant():
    if request.method == 'GET':
        return render_template('add_restaurant.html')
    elif request.method == 'POST':
        name = request.form['name']
        address = request.form['address']
        description = request.form['description']
        latitude = request.form['latitude']
        longitude = request.form['longitude']
        opening_hours = request.form['opening_hours']

        conn = get_db_connection()
        cur = conn.cursor()
        sql = """INSERT INTO restaurants (name, address, description, latitude, longitude, opening_hours) 
                 VALUES (%s, %s, %s, %s, %s, %s)"""
        cur.execute(sql, (name, address, description, latitude, longitude, opening_hours))
        conn.commit()
        cur.close()
        conn.close()
        return redirect('/admin_page')



@app.route('/edit_restaurant/<int:restaurant_id>', methods=['GET', 'POST'])
def edit_restaurant(restaurant_id):
    conn = get_db_connection()
    cur = conn.cursor()

    if request.method == 'GET':
        sql = "SELECT * FROM restaurants WHERE restaurant_id = %s"
        cur.execute(sql, (restaurant_id,))
        restaurant = cur.fetchone()
        cur.close()
        conn.close()
        return render_template('edit_restaurant.html', restaurant=restaurant)
    elif request.method == 'POST':
        name = request.form['name']
        address = request.form['address']
        description = request.form['description']
        latitude = request.form['latitude']
        longitude = request.form['longitude']
        opening_hours = request.form['opening_hours']

        sql = """UPDATE restaurants SET name = %s, address = %s, description = %s, 
                 latitude = %s, longitude = %s, opening_hours = %s WHERE restaurant_id = %s"""
        cur.execute(sql, (name, address, description, latitude, longitude, opening_hours, restaurant_id))
        conn.commit()
        cur.close()
        conn.close()
        return redirect('/admin_page')



@app.route('/delete_restaurant/<int:restaurant_id>', methods=['POST'])
def delete_restaurant(restaurant_id):
    conn = get_db_connection()
    cur = conn.cursor()
    sql = "DELETE FROM restaurants WHERE restaurant_id = %s"
    cur.execute(sql, (restaurant_id,))
    conn.commit()
    cur.close()
    conn.close()
    return redirect('/admin_page')
