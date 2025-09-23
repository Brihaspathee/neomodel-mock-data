CREATE TABLE portown.pp_prac_attrib_values (
	id integer NOT NULL,
	prac_attribute_id integer NOT NULL,
	field_id integer NOT NULL,
	value varchar NULL,
	value_date date NULL,
	value_number numeric NULL,
	label_cluster_id numeric NULL,
	CONSTRAINT pp_prac_attrib_values_pk PRIMARY KEY (id),
	CONSTRAINT pp_prac_attrib_values_fmg_attrib_fields_fk FOREIGN KEY (field_id) REFERENCES portown.fmg_attrib_fields(id),
	CONSTRAINT pp_prac_attrib_values_pp_prac_attrib_fk FOREIGN KEY (prac_attribute_id) REFERENCES portown.pp_prac_attrib(id)
);
