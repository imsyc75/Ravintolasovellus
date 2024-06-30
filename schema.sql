CREATE TABLE users(
    id SERIAL PRIMARY KEY NOT NULL,
    name TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL,
    role INTEGER NOT NULL --admin is 0, user is 1
);

CREATE TABLE categories (
    category_id SERIAL PRIMARY KEY,
    category_name VARCHAR(255) NOT NULL,
    category_type VARCHAR(255) -- ex. "cuisine" or "country"
);


CREATE TABLE restaurants (
    restaurant_id SERIAL PRIMARY KEY NOT NULL,
    name VARCHAR(255) NOT NULL,
    address TEXT NOT NULL,
    description TEXT,
    latitude NUMERIC(9,6),
    longitude NUMERIC(9,6),
    opening_hours VARCHAR(255),
    category_id INTEGER REFERENCES categories(category_id)
);


CREATE TABLE reviews (
    review_id SERIAL PRIMARY KEY NOT NULL,
    restaurant_id INTEGER REFERENCES restaurants, 
    user_id INTEGER REFERENCES users,        
    rating INTEGER,         
    comment TEXT,           
    timestamp TIMESTAMP 
);

CREATE TABLE discounts (
   discount_id SERIAL PRIMARY KEY,
   restaurant_id INTEGER NOT NULL REFERENCES restaurants(restaurant_id),
   description TEXT,
   start_date DATE,
   end_date DATE
);
