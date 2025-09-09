CREATE TABLE portown.pp_prov_loc_attrib (
	id numeric NOT NULL,
	prov_id integer NOT NULL,
	loc_id numeric NOT NULL,
	attribute_id integer NOT NULL,
	CONSTRAINT pp_prov_loc_attrib_pk PRIMARY KEY (id),
	CONSTRAINT pp_prov_loc_attrib_pp_prov_fk FOREIGN KEY (prov_id) REFERENCES portown.pp_prov(id),
	CONSTRAINT pp_prov_loc_attrib_pp_prov_tin_loc_fk FOREIGN KEY (loc_id) REFERENCES portown.pp_prov_tin_loc(id),
	CONSTRAINT pp_prov_loc_attrib_fmg_attribute_types_fk FOREIGN KEY (attribute_id) REFERENCES portown.fmg_attribute_types(id)
);

