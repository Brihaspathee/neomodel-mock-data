-- portown.pp_spec definition

-- Drop table

-- DROP TABLE portown.pp_spec;

CREATE TABLE portown.pp_spec (
	id int4 NOT NULL,
	"type" varchar NOT NULL,
	ds varchar NOT NULL,
	sitevisit_req varchar NOT NULL,
	board_cert_req bpchar(1) NULL,
	board_cert_length numeric NULL,
    ancillary varchar NULL,
	drsal varchar NULL,
	"usage" varchar NULL,
	code varchar NULL,
	label_cluster_id numeric NULL,
	CONSTRAINT pp_spec_pk PRIMARY KEY (id)
);
