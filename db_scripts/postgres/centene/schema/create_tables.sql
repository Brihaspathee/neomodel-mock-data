-- 1. Create FMG_ATTRIBUTE_TYPES table
CREATE TABLE portown.fmg_attrib_types (
	id int4 NOT NULL,
	metatype varchar NOT NULL,
	ds varchar NULL,
	category varchar NULL,
	searchable bpchar(1) NULL,
	seq_no numeric NULL,
	one_many bpchar(1) NULL,
	fmg_lock bpchar(1) NULL,
	hidden bpchar(1) NULL,
	fmg_product varchar NULL,
	CONSTRAINT fmg_attrib_types_pk PRIMARY KEY (id)
);

-- alter table portown.fmg_attrib_types
--     owner to porticoadmin;

-- 2. Create FMG_ATTRIBUTE_FIELDS table
-- portown.fmg_attrib_fields definition

-- Drop table

-- DROP TABLE portown.fmg_attrib_fields;

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
	CONSTRAINT fmg_attrib_fields_pk PRIMARY KEY (id)
);