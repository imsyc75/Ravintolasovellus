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

-- insert the restaurants information
INSERT INTO restaurants (name, address, description,latitude, longitude, opening_hours)
VALUES ('Bistro Bardot', 60.170000, 24.935000, 'A cozy bistro offering French cuisine.', 'Kluuvikatu 1, 00100 Helsinki  ', '09:00 - 21:00');

INSERT INTO restaurants (name, address, description,latitude, longitude, opening_hours)
VALUES ('Kappeli', 60.169000, 24.941000, 'Authentic Finnish cuisine, established in 186', 'Eteläesplanadi 1, 00130 Helsinki', '09:00m - 23:00');

INSERT INTO restaurants (name, address, description, latitude, longitude, opening_hours)
VALUES ('Dragon Palace', 'Kaivokatu 6, 00100 Helsinki', 'Authentic Chinese cuisine in the heart of Helsinki.', 60.1699, 24.9459, '11:30 - 22:30');

INSERT INTO restaurants (name, address, description, latitude, longitude, opening_hours)
VALUES ('Seoul Kitchen', 'Kaisaniemenkatu 1, 00100 Helsinki', 'Traditional Korean dishes with a modern twist.', 60.1721, 24.9469, '12:00 - 23:00');

INSERT INTO restaurants (name, address, description, latitude, longitude, opening_hours)
VALUES ('Bella Italia', 'Eteläesplanadi 22, 00100 Helsinki', 'Classic Italian dishes served in a cozy atmosphere.', 60.1668, 24.9482, '17:00 - 22:30');

INSERT INTO restaurants (name, address, description, latitude, longitude, opening_hours)
VALUES ('Le Petit Bistro', 'Korkeavuorenkatu 21, 00130 Helsinki', 'Charming French bistro offering authentic French cuisine.', 60.1632, 24.9478, '18:00 - 23:00');
