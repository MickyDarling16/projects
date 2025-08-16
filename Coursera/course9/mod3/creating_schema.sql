CREATE TABLE IF NOT EXISTS DimDate (
    dateid INT NOT NULL,
    date DATE NOT NULL,
    Year INT NOT NULL,
    Quarter INT NOT NULL,
    QuarterName VARCHAR(2) NOT NULL,
    Month INT NOT NULL,
    Monthname VARCHAR (11) NOT NULL,
    Day INT NOT NULL,
    Weekday  INT NOT NULL,
    WeekdayName VARCHAR (11) NOT NULL,
    PRIMARY KEY (dateid)
);

CREATE TABLE IF NOT EXISTS DimTruck (
    Truckid INT NOT NULL,
    TruckType VARCHAR (255) NOT NULL,
    PRIMARY KEY (Truckid)
);

CREATE TABLE IF NOT EXISTS DimStation (
    Stationid INT NOT NULL,
    city VARCHAR (255) NOT NULL,
    PRIMARY KEY (Stationid)
);

CREATE TABLE IF NOT EXISTS FactTrips (
    Tripid INT NOT NULL,
    Dateid INT NOT NULL,
    Stationid INT NOT NULL,
    Truckid INT NOT NULL,
    Wastecollected DECIMAL(10,2) NOT NULL,
    PRIMARY KEY (Tripid),
    Foreign Key (Dateid) REFERENCES DimDate(dateid),
    Foreign Key (Truckid) REFERENCES DimTruck(Truckid),
    Foreign Key (Stationid) REFERENCES DimStation(Stationid)
);