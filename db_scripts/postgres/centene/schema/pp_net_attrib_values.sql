CREATE TABLE portown.pp_net_attrib_values (
	id integer NOT NULL,
	net_attribute_id integer NOT NULL,
	field_id integer NOT NULL,
	value varchar NULL,
	value_date date NULL,
	value_number numeric NULL,
	label_cluster_id numeric NULL,
	CONSTRAINT pp_net_attrib_values_pk PRIMARY KEY (id),
	CONSTRAINT pp_net_attrib_values_fmg_attribute_fields_fk FOREIGN KEY (field_id) REFERENCES portown.fmg_attribute_fields(id),
	CONSTRAINT pp_net_attrib_values_pp_net_attrib_fk FOREIGN KEY (net_attribute_id) REFERENCES portown.pp_net_attrib(id)
);