-- user's name shoudle be unique
CREATE TABLE users(
    id SERIAL PRIMARY KEY NOT NULL,
    name TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL,
    role INTEGER NOT NULL
);

-- This table saves all the restaurants.
CREATE TABLE restaurants (
    restaurant_id SERIAL PRIMARY KEY NOT NULL,
    name VARCHAR(255) NOT NULL,
    address TEXT NOT NULL,
    description TEXT,
    latitude NUMERIC(9,6),
    longitude NUMERIC(9,6),
    opening_hours VARCHAR(255)
);

-- this table saves all the reviews.
CREATE TABLE reviews (
    review_id SERIAL PRIMARY KEY NOT NULL,
    restaurant_id INTEGER REFERENCES restaurants, 
    user_id INTEGER REFERENCES users,        
    rating INTEGER,         
    comment TEXT,           
    timestamp TIMESTAMP 
);

