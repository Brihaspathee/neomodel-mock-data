-- portown.fmg_codes definition

-- Drop table

-- DROP TABLE portown.fmg_codes;

CREATE TABLE portown.fmg_codes (
	code varchar NOT NULL,
	"TYPE" varchar NOT NULL,
	ds varchar NOT NULL,
	dsl varchar NULL,
	seq_no numeric NULL,
	fmg_lock bpchar(1) NULL,
	start_date date NULL,
	end_date date NULL,
	sub_type varchar NULL,
	label_cluster_id numeric NULL
);
