from flask import request, render_template, redirect, session # type: ignore
from app import app # type: ignore
from db import get_db_connection # type: ignore
from werkzeug.security import generate_password_hash, check_password_hash # type: ignore



@app.route('/')
def index():
    conn = get_db_connection()
    cur = conn.cursor()
    sql = """SELECT r.name, d.description, d.start_date, d.end_date
        FROM discounts d
        JOIN restaurants r ON d.restaurant_id = r.restaurant_id
        WHERE d.end_date >= CURRENT_DATE"""
    cur.execute(sql)
    discounts = cur.fetchall()
    cur.close()
    conn.close()
    return render_template('index.html', discounts=discounts)



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

        if not name or not password:
            return "Please fill out all fields.", 400

        conn = get_db_connection()
        cur = conn.cursor()
        try:
            sql = """SELECT name, password, role FROM users WHERE name = %s"""
            cur.execute(sql, (name,))
            user = cur.fetchone()

            if user and check_password_hash(user[1], password):
                session['username'] = user[0]
                session['role'] = user[2]  # Keep this line to use the role in session if needed
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
    session.pop('role', None)   
    return redirect('/')



@app.route('/restaurants') 
def restaurants():
    conn = get_db_connection()
    cur = conn.cursor()
    category_filter = request.args.get('category')
    if category_filter:
        sql = """SELECT r.*, c.category_name FROM restaurants r
                       JOIN categories c ON r.category_id = c.category_id
                       WHERE c.category_name = %s"""
        cur.execute(sql, (category_filter,))
    else:
        sql = """SELECT r.*, c.category_name FROM restaurants r
                       JOIN categories c ON r.category_id = c.category_id"""
        cur.execute(sql)
    restaurant_list = cur.fetchall()

    cur.execute('SELECT * FROM categories')
    categories = cur.fetchall()
    cur.close()
    conn.close()
    return render_template('restaurants.html', restaurants=restaurant_list,categories=categories)



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

    sql = "SELECT * FROM categories"
    cur.execute(sql)
    categories = cur.fetchall()
    
    sql = """SELECT d.discount_id, r.name, d.description, d.start_date, d.end_date
        FROM discounts d
        JOIN restaurants r ON d.restaurant_id = r.restaurant_id"""
    cur.execute(sql)
    discounts = cur.fetchall()
    cur.close()
    conn.close()
    return render_template('admin_page.html', restaurants=restaurants, categories=categories, discounts=discounts)



@app.route('/add_restaurant', methods=['GET', 'POST'])
def add_restaurant():
    conn = get_db_connection()
    cur = conn.cursor()
    if request.method == 'GET':
        cur.execute('SELECT * FROM categories')
        categories = cur.fetchall()
        return render_template('add_restaurant.html', categories=categories)
    elif request.method == 'POST':
        name = request.form['name']
        address = request.form['address']
        description = request.form['description']
        latitude = request.form['latitude']
        longitude = request.form['longitude']
        opening_hours = request.form['opening_hours']
        category_id = request.form['category_id']

        sql = """INSERT INTO restaurants (name, address, description, latitude, longitude, opening_hours, category_id) 
                 VALUES (%s, %s, %s, %s, %s, %s)"""
        cur.execute(sql, (name, address, description, latitude, longitude, opening_hours,category_id))
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
        cur.execute('SELECT * FROM categories')
        categories = cur.fetchall()
        cur.close()
        conn.close()
        return render_template('edit_restaurant.html', restaurant=restaurant, categories=categories)
    elif request.method == 'POST':
        name = request.form['name']
        address = request.form['address']
        description = request.form['description']
        latitude = request.form['latitude']
        longitude = request.form['longitude']
        opening_hours = request.form['opening_hours']
        category_id = request.form['category_id'] 

        sql = """UPDATE restaurants SET name = %s, address = %s, description = %s, 
                 latitude = %s, longitude = %s, opening_hours = %s, category_id = %s WHERE restaurant_id = %s"""
        cur.execute(sql, (name, address, description, latitude, longitude, opening_hours, category_id, restaurant_id))
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



@app.route('/add_category', methods=['GET', 'POST'])
def add_category():
    if request.method == 'GET':
        return render_template('add_category.html')
    elif request.method == 'POST':
        category_name = request.form['category_name']
        category_type = request.form['category_type'] 
        conn = get_db_connection()
        cur = conn.cursor()
        try:
            sql = "INSERT INTO categories (category_name, category_type) VALUES (%s, %s)"
            cur.execute(sql, (category_name, category_type))
            conn.commit()
        except Exception as e:
            conn.rollback()
            return str(e), 500
        finally:
            cur.close()
            conn.close()
        return redirect('/admin_page')




@app.route('/delete_category/<int:category_id>', methods=['POST'])
def delete_category(category_id):
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        sql = "DELETE FROM categories WHERE category_id = %s"
        cur.execute(sql, (category_id,))
        conn.commit()
    except Exception as e:
        conn.rollback()
        return str(e), 500
    finally:
        cur.close()
        conn.close()
    return redirect('/admin_page')



@app.route('/search')
def search():
    query = request.args.get('q', '')
    if query:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT restaurant_id FROM restaurants WHERE name LIKE %s", ('%' + query + '%',))
        restaurant = cur.fetchone()
        cur.close()
        conn.close()
        if restaurant:
            return redirect(f'/restaurant/{restaurant[0]}')
        else:
            return render_template('error.html', query=query)
    return render_template('index.html')



@app.route('/add_discount', methods=['GET', 'POST'])
def add_discount():
   if request.method == 'POST':
       try:
           restaurant_name = request.form['restaurant_name']
           description = request.form['description']
           start_date = request.form['start_date']
           end_date = request.form['end_date']


           conn = get_db_connection()
           cur = conn.cursor()
           cur.execute("SELECT restaurant_id FROM restaurants WHERE name = %s", (restaurant_name,))
           print(f"Executing SQL: SELECT restaurant_id FROM restaurants WHERE name = '{restaurant_name}'")
           restaurant = cur.fetchone()


           if restaurant:
               restaurant_id = restaurant[0]
               sql = 'INSERT INTO discounts (restaurant_id, description, start_date, end_date) VALUES (%s, %s, %s, %s)'
               cur.execute(sql, (restaurant_id, description, start_date, end_date))
               conn.commit()
           else:
               return "No restaurant found with that name."
           return redirect('/admin_page')
       except Exception as e:
           conn.rollback()  # Rollback in case of any error
           return f"An error occurred: {str(e)}"
       finally:
           cur.close()
           conn.close()
   else:
       conn = get_db_connection()
       cur = conn.cursor()
       cur.execute("SELECT restaurant_id, name FROM restaurants")
       restaurants = cur.fetchall()
       cur.close()
       conn.close()
       return render_template('add_discount.html', restaurants=restaurants)