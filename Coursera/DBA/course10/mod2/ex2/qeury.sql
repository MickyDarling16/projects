SELECT
    co.country,
    ca.category,
    SUM(amount) AS TotalSales
FROM "FactSales" f
JOIN "DimCountry" co ON f.countryid = co.countryid
JOIN "DimCategory" ca ON f.categoryid = ca.categoryid
GROUP BY
    GROUPING SETS (
        (co.country),
        (ca.category),
        ()
    );


SELECT
    dd.Year,
    co.country,
    SUM(f.amount) AS TotalSales
FROM "FactSales" f
JOIN "DimCountry" co ON f.countryid = co.countryid
JOIN "DimDate" dd ON f.dateid = dd.dateid
GROUP BY
    ROLLUP(co.country, dd.Year);


SELECT
    dd.Year,
    co.country,
    AVG(f.amount) AS "Average Sales"
FROM "FactSales" f
JOIN "DimCountry" co ON f.countryid = co.countryid
JOIN "DimDate" dd ON f.dateid = dd.dateid
GROUP BY
    CUBE(co.country, dd.Year);


CREATE MATERIALIZED VIEW total_sales_per_country (country, total_sales) AS
SELECT
	co.country,
    SUM(f.amount) AS total_sales
FROM "FactSales" f
JOIN "DimCountry" co ON f.countryid = co.countryid
GROUP BY co.country;
