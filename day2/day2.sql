CREATE DATABASE online_store;

USE online_store;

CREATE TABLE categories (
    category_id INT PRIMARY KEY AUTO_INCREMENT,
    category_name VARCHAR(50) NOT NULL UNIQUE
);

-- 2. Customers Table (Parent to Orders)
CREATE TABLE customers (
    customer_id INT PRIMARY KEY AUTO_INCREMENT,
    customer_name VARCHAR(50) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE
);

-- 3. Products Table (Child of Categories)
CREATE TABLE products (
    product_id INT PRIMARY KEY AUTO_INCREMENT,
    product_name VARCHAR(50) NOT NULL,
    category_id INT NOT NULL,
    price DECIMAL(10, 2) NOT NULL CHECK (price > 0),
    CONSTRAINT fk_products_categories
        FOREIGN KEY (category_id) REFERENCES categories(category_id)
        ON UPDATE CASCADE ON DELETE RESTRICT
);

-- 4. Orders Table (Child of Customers)
CREATE TABLE orders (
    order_id INT PRIMARY KEY AUTO_INCREMENT,
    customer_id INT NOT NULL,
    order_date DATE DEFAULT (CURRENT_DATE),
    order_status VARCHAR(20) DEFAULT 'Pending',
    CONSTRAINT fk_orders_customers
        FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
        ON UPDATE CASCADE ON DELETE CASCADE
);

-- 5. Order Items Table (Junction Table linking Orders and Products)
CREATE TABLE order_items (
    order_item_id INT PRIMARY KEY AUTO_INCREMENT,
    order_id INT NOT NULL,
    product_id INT NOT NULL,
    quantity INT NOT NULL CHECK (quantity > 0),
    CONSTRAINT fk_order_items_orders
        FOREIGN KEY (order_id) REFERENCES orders(order_id)
        ON UPDATE CASCADE ON DELETE CASCADE,
    CONSTRAINT fk_order_items_products
        FOREIGN KEY (product_id) REFERENCES products(product_id)
        ON UPDATE CASCADE ON DELETE RESTRICT
);

INSERT INTO categories (category_name) VALUES
('Electronics'),
('Books'),
('Clothing'),
('Home & Kitchen'),
('Sports & Outdoors');

-- Populate Customers
INSERT INTO customers (customer_name, email) VALUES
('Alice Smith', 'alice@example.com'),
('Bob Jones', 'bob@example.com'),
('Charlie Brown', 'charlie@example.com'),
('Diana Prince', 'diana@example.com'),
('Evan Wright', 'evan@example.com');

-- Populate Products
INSERT INTO products (product_name, category_id, price) VALUES
('Wireless Mouse', 1, 25.99),
('Mechanical Keyboard', 1, 89.50),
('SQL Guidebook', 2, 45.00),
('Cotton T-Shirt', 3, 19.99),
('Stainless Steel Water Bottle', 5, 15.00);

-- Populate Orders
INSERT INTO orders (customer_id, order_date, order_status) VALUES
(1, '2026-10-01', 'Shipped'),
(2, '2026-10-02', 'Pending'),
(3, '2026-10-03', 'Delivered'),
(1, '2026-10-04', 'Delivered'),
(4, '2026-10-05', 'Cancelled');

-- Populate Order Items
INSERT INTO order_items (order_id, product_id, quantity) VALUES
(1, 1, 2),
(1, 3, 1),
(2, 2, 1),
(3, 4, 3),
(4, 5, 2);




ALTER TABLE customers 
ADD phone_number VARCHAR(15);


UPDATE customers 
SET phone_number = '9876543210' 
WHERE customer_id = 1;


DELETE FROM orders 
WHERE order_status = 'Cancelled';




-- INNER JOIN
SELECT 
    orders.order_id, 
    customers.customer_name, 
    orders.order_date, 
    orders.order_status
FROM orders
INNER JOIN customers ON orders.customer_id = customers.customer_id;

-- LEFT JOIN
SELECT 
    customers.customer_id, 
    customers.customer_name, 
    orders.order_id, 
    orders.order_status
FROM customers
LEFT JOIN orders ON customers.customer_id = orders.customer_id;

-- GROUP BY with HAVING
SELECT 
    customer_id, 
    COUNT(order_id) AS total_orders
FROM orders
GROUP BY customer_id
HAVING COUNT(order_id) > 1;

-- SUBQUERY
SELECT 
    product_name, 
    price
FROM products
WHERE price > (
    SELECT AVG(price) 
    FROM products
);



-- View 1: Active orders summary
CREATE VIEW active_orders AS
SELECT order_id, customer_id, order_date, order_status
FROM orders
WHERE order_status != 'Delivered';

-- View 2: High value products (priced above $30)
CREATE VIEW expensive_products AS
SELECT product_id, product_name, price
FROM products
WHERE price > 30.00;

-- Index: Speed up searches by customer email
CREATE INDEX idx_customer_email 
ON customers(email);