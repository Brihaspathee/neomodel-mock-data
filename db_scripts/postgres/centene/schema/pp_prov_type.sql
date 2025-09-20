-- portown.pp_prov_type definition

-- Drop table

-- DROP TABLE portown.pp_prov_type;

CREATE TABLE portown.pp_prov_type (
	id int4 NOT NULL,
	type_ds varchar NOT NULL,
	category varchar NULL,
	subcategory varchar NULL,
	fmg_lock varchar NULL,
	label_cluster_id varchar NULL,
	"usage" varchar NULL,
	CONSTRAINT pp_prov_type_pk PRIMARY KEY (id)
);

