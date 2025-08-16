
-- Grouping Sets query: stationid, trucktype, total waste collected
SELECT
	ft.Stationid,
	dt.TruckType,
	SUM(ft.Wastecollected) AS TotalWasteCollected
FROM FactTrips ft
JOIN DimTruck dt ON ft.Truckid = dt.Truckid -- INNER JOIN IS SAME AS JOIN
GROUP BY GROUPING SETS (
	(Stationid),
	(TruckType),
	(Stationid, TruckType),
	()
);


-- Rollup query: Total waste collected by year, city, and stationid, including subtotals and grand total
SELECT
	dd.Year,
	ds.city,
	ft.Stationid,
	SUM(ft.Wastecollected) AS TotalWasteCollected
FROM FactTrips ft
JOIN DimDate dd ON ft.Dateid = dd.dateid
JOIN DimStation ds ON ft.Stationid = ds.Stationid
GROUP BY ROLLUP (dd.Year, ds.city, ft.Stationid);


-- Cube query: Average waste collected by year, city, and stationid
SELECT
	dd.Year,
	ds.city,
	ft.Stationid,
	AVG(ft.Wastecollected) AS AvgWasteCollected
FROM FactTrips ft
JOIN DimDate dd ON ft.Dateid = dd.dateid
JOIN DimStation ds ON ft.Stationid = ds.Stationid
GROUP BY CUBE (dd.Year, ds.city, ft.Stationid);


-- Materialized view: Maximum waste collected by city, station, and truck type
CREATE MATERIALIZED VIEW max_waste_stats (city, Stationid, TruckType) AS
SELECT
	ds.city,
	ft.Stationid,
	dt.TruckType,
	MAX(ft.Wastecollected) AS MaxWasteCollected
FROM FactTrips ft
JOIN DimStation ds ON ft.Stationid = ds.Stationid
JOIN DimTruck dt ON ft.Truckid = dt.Truckid
GROUP BY ds.city, ft.Stationid, dt.TruckType;

