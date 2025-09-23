CREATE TABLE portown.pp_prac (
	id integer NOT NULL,
	fname varchar NULL,
	mname varchar NULL,
	lname varchar NULL,
	xname varchar NULL,
	"degree" varchar NULL,
	sex char(1) NULL,
	dob date NULL,
	ssn varchar NULL,
	email varchar NULL,
	salutation varchar NULL,
	label_cluster_id numeric NULL,
	prac_type_id numeric NULL,
	narrative varchar NULL,
	CONSTRAINT pp_prac_pk PRIMARY KEY (id)
);
