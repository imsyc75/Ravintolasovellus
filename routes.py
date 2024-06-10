from flask import request, render_template, redirect, session # type: ignore
from app import app # type: ignore
from db import get_db_connection # type: ignore


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
        role = 1 # Defaults to 1, and can be set by the administrator.

        conn = get_db_connection()
        cur = conn.cursor()

        try:
            sql = """SELECT * FROM users WHERE name = %s"""
            cur.execute(sql, (name,))
            if cur.fetchone():
                return 'Username already exists', 400
            
            sql = """INSERT INTO users (name, password, role) 
            VALUES (%s, crypt(%s, gen_salt('bf')), %s)"""
            cur.execute(sql ,(name, password, role))
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
        name = request.form['name']
        password = request.form['password']

        conn = get_db_connection()
        cur = conn.cursor()
        try:
            sql = """SELECT password FROM users WHERE name = %s 
            AND password = crypt(%s, password)"""
            cur.execute(sql, (name, password))
            if cur.fetchone():
                session['username'] = name
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


#see the restaurants information
@app.route('/restaurant/<int:restaurant_id>')
def restaurant_detail(restaurant_id):
    conn = get_db_connection()
    cur = conn.cursor()
    sql = """SELECT * FROM restaurants WHERE restaurant_id = %s"""
    cur.execute(sql, (restaurant_id,))
    restaurant = cur.fetchone()

    if not restaurant:
        return "Restaurant not found", 404
    
    sql = """ SELECT r.*, u.name  
              FROM reviews r JOIN users u ON r.user_id = u.id 
              WHERE r.restaurant_id = %s"""
    cur.execute(sql, (restaurant_id,))
    reviews = cur.fetchall()

    cur.close()
    conn.close()
    return render_template('restaurant_detail.html', restaurant=restaurant, reviews=reviews)


#add review of restaurants
@app.route('/restaurant/<int:restaurant_id>/add_review', methods=['POST'])
def add_review(restaurant_id):
    if 'username' not in session:
        return redirect('/login')
    
    conn = get_db_connection()
    cur = conn.cursor()
    sql = """""SELECT id FROM users WHERE name = %s"""
    cur.execute(sql, (session['username'],))
    user = cur.fetchone()
    if not user:
        return 'User not found', 404

    comment = request.form['comment']
    rating = float(request.form['rating'])
    sql = """"INSERT INTO reviews (restaurant_id, user_id, rating, comment) VALUES (%s, %s, %s, %s)""""
    cur.execute(sql,(restaurant_id, user[0], rating, comment))
    conn.commit()
    cur.close()
    conn.close()
    return redirect(f'/restaurant/{restaurant_id}')
