-- portown.fmg_counties definition

CREATE TABLE portown.fmg_counties (
	id int4 NOT NULL,
	ds varchar NOT NULL,
	CONSTRAINT fmg_counties_pk PRIMARY KEY (id)
);