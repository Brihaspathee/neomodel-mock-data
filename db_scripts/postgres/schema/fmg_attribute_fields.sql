-- portown.fmg_attribute_fields definition

-- Drop table

-- DROP TABLE portown.fmg_attribute_fields;

CREATE TABLE portown.fmg_attrib_fields (
	id int4 NOT NULL,
	attribute_id int4 NOT NULL,
	fmgcode varchar NULL,
	fieldname varchar NOT NULL,
	"datatype" varchar NOT NULL,
	order_by varchar NULL,
	category varchar(25) NULL,
	read_only bpchar(1) NULL,
	lookup_query varchar(2000) NULL,
	fmg_lock bpchar(1) NULL,
	fieldlength numeric NULL,
	mask varchar(30) NULL,
	pe_ind bpchar(1) NULL,
	CONSTRAINT fmg_attribute_fields_pk PRIMARY KEY (id)
);


-- portown.fmg_attribute_fields foreign keys

ALTER TABLE portown.fmg_attribute_fields ADD CONSTRAINT fmg_attribute_fields_fmg_attribute_types_id_fk FOREIGN KEY (attribute_id) REFERENCES portown.fmg_attribute_types(id);