CREATE TABLE portown.pp_prov_loc_ofhours (
	id integer NOT NULL,
	prov_id integer NOT NULL,
	loc_id integer NOT NULL,
	"event" varchar NOT NULL,
	dayofweek varchar NOT NULL,
	"time" varchar NOT NULL,
	CONSTRAINT pp_prov_loc_ofhours_pk PRIMARY KEY (id),
	CONSTRAINT pp_prov_loc_ofhours_pp_prov_fk FOREIGN KEY (prov_id) REFERENCES portown.pp_prov(id),
	CONSTRAINT pp_prov_loc_ofhours_pp_prov_tin_loc_fk FOREIGN KEY (loc_id) REFERENCES portown.pp_prov_tin_loc(id)
);
