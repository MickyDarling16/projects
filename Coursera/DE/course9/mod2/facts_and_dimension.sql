BEGIN;

CREATE TABLE public."DimStore" (
    "storeid" INT NOT NULL,
    "country" VARCHAR (20) NOT NULL,
    "city" VARCHAR (50) NOT NULL,
    PRIMARY KEY (storeid)
);

CREATE TABLE public."DimDate" (
    "dateID" INT NOT NULL,
    "day_num" INT NOT NULL,
    "weekday_num" INT NOT NULL,
    "weekday_name" VARCHAR (11) NOT NULL,
    "month_num" INT NOT NULL,
    "month_name" VARCHAR (11) NOT NULL,
    "year" INT NOT NULL,
    "quarter_num" INT NOT NULL,
    "quarter_name" VARCHAR (3) NOT NULL,
    PRIMARY KEY (dateID)
);

CREATE TABLE public."FactSales" (
    "rowid" INT NOT NULL,
    "storeid" INT NOT NULL,
    "dateID" INT NOT NULL,
    "totalsale" INT NOT NULL,
    PRIMARY KEY (rowid)
);


ALTER TABLE public."FactSales"
    ADD FOREIGN KEY (storeid) REFERENCES public."DimStore" (storeid) NOT VALID;

ALTER TABLE public."FactSales"
    ADD FOREIGN KEY (dateID) REFERENCES public."DimDate" (dateID) NOT VALID;


END;