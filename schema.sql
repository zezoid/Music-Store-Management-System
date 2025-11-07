CREATE DATABASE IF NOT EXISTS music_store;
USE music_store;

CREATE TABLE customer (
    customer_id INT AUTO_INCREMENT PRIMARY KEY,
    full_name VARCHAR(100),
    email VARCHAR(100),
    country VARCHAR(50)
);

CREATE TABLE artist (
    artist_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100)
);

CREATE TABLE album (
    album_id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(100),
    artist_id INT,
    FOREIGN KEY (artist_id) REFERENCES artist(artist_id) ON DELETE CASCADE
);

CREATE TABLE track (
    track_id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(100),
    album_id INT,
    unit_price DECIMAL(10,2),
    stock_quantity INT DEFAULT 20,
    FOREIGN KEY (album_id) REFERENCES album(album_id) ON DELETE CASCADE
);

CREATE TABLE orders (
    order_id INT AUTO_INCREMENT PRIMARY KEY,
    customer_id INT,
    order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    total_amount DECIMAL(10,2) DEFAULT 0,
    FOREIGN KEY (customer_id) REFERENCES customer(customer_id) ON DELETE CASCADE
);

CREATE TABLE order_item (
    order_item_id INT AUTO_INCREMENT PRIMARY KEY,
    order_id INT,
    track_id INT,
    quantity INT,
    unit_price DECIMAL(10,2),
    line_total DECIMAL(10,2),
    FOREIGN KEY (order_id) REFERENCES orders(order_id) ON DELETE CASCADE,
    FOREIGN KEY (track_id) REFERENCES track(track_id) ON DELETE CASCADE
);
