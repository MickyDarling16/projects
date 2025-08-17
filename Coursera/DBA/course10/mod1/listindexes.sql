USE sales;

CREATE INDEX ts ON sales_data(timestamp);

SHOW INDEX FROM sales_data;