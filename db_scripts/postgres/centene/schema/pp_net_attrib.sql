CREATE TABLE portown.pp_net_attrib (
	id integer NOT NULL,
	net_id integer NOT NULL,
	attribute_id integer NOT NULL,
	CONSTRAINT pp_net_attrib_pk PRIMARY KEY (id),
	CONSTRAINT pp_net_attrib_fmg_attribute_types_fk FOREIGN KEY (attribute_id) REFERENCES portown.fmg_attrib_types(id),
	CONSTRAINT pp_net_attrib_pp_net_fk FOREIGN KEY (net_id) REFERENCES portown.pp_net(id)
);