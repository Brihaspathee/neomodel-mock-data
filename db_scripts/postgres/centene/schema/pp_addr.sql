-- portown.pp_addr definition

CREATE TABLE portown.pp_addr (
	id int4 NOT NULL,
	"type" varchar NULL,
	addr1 varchar NOT NULL,
	addr2 varchar NULL,
	addr3 varchar NULL,
	city_id int4 NOT NULL,
	county_id int4 NOT NULL,
	county_fips varchar NULL,
	zip varchar NOT NULL,
	latitude varchar NULL,
	longitude varchar NULL,
	start_date date NULL,
	end_date date NULL,
	plus4 varchar NULL,
	postal_code varchar NULL,
	country_id varchar NULL,
	ugly_addr1 varchar NULL,
	ugly_addr2 varchar NULL,
	latitude7 varchar NULL,
	longitude7 varchar NULL,
	CONSTRAINT id PRIMARY KEY (id)
);


-- portown.pp_addr foreign keys

ALTER TABLE portown.pp_addr ADD CONSTRAINT pp_addr_fmg_cities_fk FOREIGN KEY (city_id) REFERENCES portown.fmg_cities(id);
ALTER TABLE portown.pp_addr ADD CONSTRAINT pp_addr_fmg_counties_fk FOREIGN KEY (county_id) REFERENCES portown.fmg_counties(id);