CREATE TABLE portown.pp_prac_loc_attrib (
	id integer NOT NULL,
	prac_id integer NOT NULL,
	prov_id integer NOT NULL,
	loc_id integer NOT NULL,
	attribute_id integer NOT NULL,
	CONSTRAINT pp_prac_loc_attrib_pk PRIMARY KEY (id),
	CONSTRAINT pp_prac_loc_attrib_fmg_attrib_types_fk FOREIGN KEY (attribute_id) REFERENCES portown.fmg_attrib_types(id),
	CONSTRAINT pp_prac_loc_attrib_pp_prac_fk FOREIGN KEY (prac_id) REFERENCES portown.pp_prac(id),
	CONSTRAINT pp_prac_loc_attrib_pp_prov_fk FOREIGN KEY (prov_id) REFERENCES portown.pp_prov(id),
	CONSTRAINT pp_prac_loc_attrib_pp_prov_tin_loc_fk FOREIGN KEY (loc_id) REFERENCES portown.pp_prov_tin_loc(id)
);
