-- portown.pp_prov_tin definition

CREATE TABLE portown.pp_prov_tin (
	id int4 NOT NULL,
	"name" varchar NOT NULL,
	tin varchar NOT NULL,
	"type" varchar NULL,
	label_cluster_id varchar NULL,
	CONSTRAINT pp_prov_tin_pk PRIMARY KEY (id)
);

