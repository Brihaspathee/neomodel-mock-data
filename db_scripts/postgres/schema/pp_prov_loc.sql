CREATE TABLE portown.pp_prov_loc (
	prov_id integer NOT NULL,
	loc_id integer NOT NULL,
	name_usage char(1) NULL,
	"primary" char(1) NULL,
	start_date date NULL,
	end_date date NULL,
	print_supress char(1) NULL,
	CONSTRAINT pp_prov_loc_pp_prov_fk FOREIGN KEY (prov_id) REFERENCES portown.pp_prov(id),
	CONSTRAINT pp_prov_loc_pp_prov_tin_loc_fk FOREIGN KEY (loc_id) REFERENCES portown.pp_prov_tin_loc(id)
);