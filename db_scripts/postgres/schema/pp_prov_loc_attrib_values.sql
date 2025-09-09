CREATE TABLE portown.pp_prov_loc_attrib_values (
	id varchar NOT NULL,
	prov_loc_attribute_id numeric NOT NULL,
	field_id integer NOT NULL,
	value varchar NULL,
	value_date date NULL,
	value_number numeric NULL,
	CONSTRAINT pp_prov_loc_attrib_values_pk PRIMARY KEY (id),
	CONSTRAINT pp_prov_loc_attrib_values_pp_prov_loc_attrib_fk FOREIGN KEY (prov_loc_attribute_id) REFERENCES portown.pp_prov_loc_attrib(id),
	CONSTRAINT pp_prov_loc_attrib_values_fmg_attribute_fields_fk FOREIGN KEY (field_id) REFERENCES portown.fmg_attribute_fields(id)
);