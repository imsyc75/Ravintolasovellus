CREATE TABLE users(
    id SERIAL PRIMARY KEY NOT NULL,
    name TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL,
    role INTEGER NOT NULL --admin is 0, user is 1
);

CREATE TABLE categories (
    category_id INT PRIMARY KEY,
    category_name VARCHAR(255) NOT NULL,
    category_type VARCHAR(255) NOT NULL  -- ex. "cuisine" or "country"
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



-- insert the categories information
INSERT INTO categories (category_id, category_name, category_type) VALUES (1, 'Finnish', 'country');
INSERT INTO categories (category_id, category_name, category_type) VALUES (2, 'French', 'country');
INSERT INTO categories (category_id, category_name, category_type) VALUES (3, 'Chinese', 'country');

-- insert the restaurants information
INSERT INTO restaurants (name, address, description, latitude, longitude, opening_hours, category_id)
VALUES ('Bistro Bardot', 'Kluuvikatu 1, 00100 Helsinki', 'A cozy bistro offering French cuisine.', 60.170000, 24.935000, '09:00 - 21:00', 2);

INSERT INTO restaurants (name, address, description, latitude, longitude, opening_hours, category_id)
VALUES ('Kappeli', 'Eteläesplanadi 1, 00130 Helsinki', 'Authentic Finnish cuisine, established in 1867', 60.169000, 24.941000, '09:00 - 23:00', 1);

INSERT INTO restaurants (name, address, description, latitude, longitude, opening_hours, category_id)
VALUES ('Dragon Palace', 'Kaivokatu 6, 00100 Helsinki', 'Authentic Chinese cuisine in the heart of Helsinki.', 60.1699, 24.9459, '11:30 - 22:30', 3);

INSERT INTO restaurants (name, address, description, latitude, longitude, opening_hours, category_id)
VALUES ('Le Petit Bistro', 'Korkeavuorenkatu 21, 00130 Helsinki', 'Charming French bistro offering authentic French cuisine.', 60.1632, 24.9478, '18:00 - 23:00', 2);