-- portown.fmg_attribute_types definition

-- Drop table

-- DROP TABLE portown.fmg_attribute_types;

CREATE TABLE portown.fmg_attribute_types (
	id int4 NOT NULL,
	metatype varchar NOT NULL,
	description varchar NULL,
	category varchar NULL,
	searchable bpchar(1) NULL,
	seq_no numeric NULL,
	one_many bpchar(1) NULL,
	fmg_lock bpchar(1) NULL,
	hidden bpchar(1) NULL,
	fmg_product varchar NULL,
	CONSTRAINT fmg_attribute_types_pk PRIMARY KEY (id)
);