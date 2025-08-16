BEGIN;

CREATE TABLE IF NOT EXIST "MyDimDate" (
    "dateid" INT NOT NULL,
    "year" INT NOT NULL,
    "Quarter" INT NOT NULL,
    "QuarterName" VARCHAR(2) NOT NULL,
    "month_num" INT NOT NULL,
    "month_name" VARCHAR (11) NOT NULL,
    "day_of_month_num" INT NOT NULL,
    "day_of_week_name" VARCHAR (11) NOT NULL,
    "day_of_week_num" INT NOT NULL,
    PRIMARY (dateid)
);

CREATE TABLE IF NOT EXIST "MyDimProduct" (
    "productid" INT NOT NULL,
    "product_type" VARCHAR (50) NOT NULL,
    PRIMARY (productid)
);

CREATE TABLE IF NOT EXIST "MyDimCustomerSegment" (
    "customerid" INT NOT NULL,
    "city" VARCHAR (255) NOT NULL,
    "segmentname" VARCHAR (255) NOT NULL,
    PRIMARY (customerid)
);

CREATE TABLE IF NOT EXIST "MyDimCustomerSegment" (
    "salesid" INT NOT NULL,
    "price_per_unit" DECIMAL(10,2) NOT NULL,
    "quantity_sold" INT NOT NULL,
    "productid" INT NOT NULL,
    "customerid" INT NOT NULL,
    "dateid" INT NOT NULL,
    PRIMARY (salesid)
    Foreign Key (productid) REFERENCES MyDimProduct(productid),
    Foreign Key (customerid) REFERENCES MyDimCustomerSegment(customerid),
    Foreign Key (dateid) REFERENCES MyDimDate(dateid)
);

END;