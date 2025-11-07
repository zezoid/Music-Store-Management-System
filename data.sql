-- Use the music_store database
USE music_store;

-- Disable safe update mode (important for batch updates)
SET SQL_SAFE_UPDATES = 0;

-- ==========================
--  CUSTOMERS
-- ==========================
INSERT INTO customer (full_name, email, country) VALUES
('John Smith', 'john.smith@example.com', 'USA'),
('Emma Johnson', 'emma.johnson@example.com', 'UK'),
('Raj Mehta', 'raj.mehta@example.com', 'India'),
('Maria Lopez', 'maria.lopez@example.com', 'Spain'),
('Liam Brown', 'liam.brown@example.com', 'Canada'),
('Sophia Chen', 'sophia.chen@example.com', 'China'),
('Oliver Garcia', 'oliver.garcia@example.com', 'Mexico'),
('Ava Rossi', 'ava.rossi@example.com', 'Italy'),
('Noah Müller', 'noah.muller@example.com', 'Germany'),
('Isabella Silva', 'isabella.silva@example.com', 'Brazil'),
('Ethan Tan', 'ethan.tan@example.com', 'Singapore'),
('Mia Dubois', 'mia.dubois@example.com', 'France'),
('Lucas Evans', 'lucas.evans@example.com', 'Australia'),
('Amelia Ivanova', 'amelia.ivanova@example.com', 'Russia'),
('Daniel Kim', 'daniel.kim@example.com', 'South Korea');

-- ==========================
--  ARTISTS
-- ==========================
INSERT INTO artist (name) VALUES
('Coldplay'),
('Adele'),
('Arijit Singh'),
('Taylor Swift'),
('Ed Sheeran'),
('Imagine Dragons'),
('Billie Eilish'),
('The Weeknd');

-- ==========================
--  ALBUMS
-- ==========================
INSERT INTO album (title, artist_id) VALUES
('Parachutes', 1),
('A Head Full of Dreams', 1),
('25', 2),
('30', 2),
('Tum Hi Ho', 3),
('Love Dose', 3),
('1989', 4),
('Reputation', 4),
('Divide', 5),
('Evolve', 6),
('When We All Fall Asleep', 7),
('After Hours', 8);

-- ==========================
--  TRACKS
-- ==========================
INSERT INTO track (title, album_id, unit_price, stock_quantity) VALUES
('Yellow', 1, 2.99, 25),
('Shiver', 1, 2.49, 18),
('Fix You', 2, 3.49, 20),
('Adventure of a Lifetime', 2, 3.29, 22),

('Hello', 3, 2.49, 16),
('Send My Love', 3, 2.59, 14),
('Easy On Me', 4, 3.19, 19),
('I Drink Wine', 4, 3.29, 12),

('Tum Hi Ho', 5, 1.99, 30),
('Raabta', 5, 2.29, 25),
('Muskurane', 6, 2.19, 22),
('Love Dose', 6, 1.99, 18),

('Blank Space', 7, 2.79, 15),
('Style', 7, 2.99, 17),
('Look What You Made Me Do', 8, 3.49, 10),
('Delicate', 8, 3.19, 12),

('Shape of You', 9, 3.59, 20),
('Perfect', 9, 3.49, 25),
('Castle on the Hill', 9, 3.09, 22),

('Believer', 10, 3.29, 25),
('Thunder', 10, 3.19, 24),
('Whatever It Takes', 10, 2.99, 26),

('Bad Guy', 11, 3.39, 20),
('You Should See Me in a Crown', 11, 3.19, 18),
('Bury a Friend', 11, 3.09, 21),

('Blinding Lights', 12, 3.59, 25),
('Save Your Tears', 12, 3.39, 22),
('In Your Eyes', 12, 3.19, 18),
('After Hours', 12, 3.49, 20),
('Heartless', 12, 3.29, 19);

-- ==========================
--  ORDERS
-- ==========================
INSERT INTO orders (customer_id, order_date, total_amount) VALUES
(1, '2025-10-01 10:23:00', 0),
(2, '2025-10-03 14:12:00', 0),
(3, '2025-10-05 09:40:00', 0),
(4, '2025-10-07 11:25:00', 0),
(5, '2025-10-08 15:00:00', 0),
(6, '2025-10-10 17:45:00', 0),
(7, '2025-10-11 18:10:00', 0),
(8, '2025-10-12 16:30:00', 0),
(9, '2025-10-13 20:45:00', 0),
(10, '2025-10-15 09:00:00', 0);

-- ==========================
--  ORDER ITEMS
-- ==========================
INSERT INTO order_item (order_id, track_id, quantity, unit_price, line_total) VALUES
(1, 1, 2, 2.99, 5.98),
(1, 18, 1, 3.49, 3.49),
(2, 20, 2, 3.29, 6.58),
(2, 26, 1, 3.59, 3.59),
(3, 9, 3, 1.99, 5.97),
(3, 11, 2, 2.19, 4.38),
(4, 13, 1, 2.79, 2.79),
(4, 15, 2, 3.49, 6.98),
(5, 24, 1, 3.39, 3.39),
(5, 28, 1, 3.19, 3.19),
(6, 26, 2, 3.59, 7.18),
(6, 10, 1, 2.29, 2.29),
(7, 2, 1, 2.49, 2.49),
(7, 3, 2, 3.49, 6.98),
(8, 27, 2, 3.39, 6.78),
(8, 25, 1, 3.19, 3.19),
(9, 19, 3, 3.49, 10.47),
(9, 29, 1, 3.49, 3.49),
(10, 21, 2, 3.19, 6.38),
(10, 23, 1, 3.09, 3.09);

-- ==========================
--  UPDATE TOTAL AMOUNTS
-- ==========================
UPDATE orders o
JOIN (
    SELECT order_id, SUM(line_total) AS sum_total
    FROM order_item
    GROUP BY order_id
) x
ON o.order_id = x.order_id
SET o.total_amount = x.sum_total
WHERE o.order_id > 0;

-- Re-enable safe updates
SET SQL_SAFE_UPDATES = 1;

-- Done!
