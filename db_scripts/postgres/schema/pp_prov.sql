-- portown.pp_prov definition


CREATE TABLE portown.pp_prov (
	id int4 NOT NULL,
	"name" varchar NOT NULL,
	tin_id int4 NOT NULL,
	prov_type_id int4 NOT NULL,
	address_id int4 NOT NULL,
	spec_id int4 NOT NULL,
	sub_prov_code varchar NULL,
	name_usage varchar NULL,
	medicare_no varchar NULL,
	label_cluster_id varchar NULL,
	CONSTRAINT pp_prov_pk PRIMARY KEY (id)
);


-- portown.pp_prov foreign keys

ALTER TABLE portown.pp_prov ADD CONSTRAINT pp_prov_pp_addr_id_fk FOREIGN KEY (address_id) REFERENCES portown.pp_addr(id);
ALTER TABLE portown.pp_prov ADD CONSTRAINT pp_prov_pp_prov_tin_id_fk FOREIGN KEY (tin_id) REFERENCES portown.pp_prov_tin(id);
ALTER TABLE portown.pp_prov ADD CONSTRAINT pp_prov_pp_prov_type_id_fk FOREIGN KEY (prov_type_id) REFERENCES portown.pp_prov_type(id);
ALTER TABLE portown.pp_prov ADD CONSTRAINT pp_prov_pp_spec_id_fk FOREIGN KEY (spec_id) REFERENCES portown.pp_spec(id);