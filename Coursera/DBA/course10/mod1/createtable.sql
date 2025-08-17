-- This SQL is query is for the MySQL Server

DROP DATABASE IF EXISTS sales;
CREATE DATABASE sales;

USE sales;
DROP TABLE IF EXISTS sales_data;

CREATE TABLE sales_data (
    productid INT NOT NULL,
    customerid INT NOT NULL,
    price DECIMAL(10, 2) NOT NULL,
    quantity INT NOT NULL,
    timestamp TIMESTAMP NOT NULL
);