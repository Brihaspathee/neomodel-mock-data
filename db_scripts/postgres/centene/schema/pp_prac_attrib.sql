CREATE TABLE portown.pp_prac_attrib (
	id integer NOT NULL,
	prac_id integer NOT NULL,
	attribute_id integer NOT NULL,
	CONSTRAINT pp_prac_attrib_pk PRIMARY KEY (id),
	CONSTRAINT pp_prac_attrib_fmg_attrib_types_fk FOREIGN KEY (attribute_id) REFERENCES portown.fmg_attrib_types(id),
	CONSTRAINT pp_prac_attrib_pp_prac_fk FOREIGN KEY (prac_id) REFERENCES portown.pp_prac(id)
);
