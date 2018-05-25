DROP TABLE IF EXISTS product
DROP TABLE IF EXISTS category
DROP TABLE IF EXISTS store
CREATE TABLE product (code BIGINT UNSIGNED PRIMARY KEY, name VARCHAR(100) NOT NULL, brand VARCHAR(100) NOT NULL, url VARCHAR(255) NOT NULL, nutriscore CHAR(1) NOT NULL)
CREATE TABLE category (id TINYINT UNSIGNED PRIMARY KEY AUTO_INCREMENT, name VARCHAR(100) NOT NULL)
CREATE TABLE store (id INT UNSIGNED PRIMARY KEY AUTO_INCREMENT, name VARCHAR(100))