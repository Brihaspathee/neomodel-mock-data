CREATE TABLE portown.pc_prac_training (
	id integer NOT NULL,
	prac_id integer NOT NULL,
	institution_id integer NULL,
	specialty_id integer NULL,
	"TYPE" varchar NULL,
	start_date date NULL,
	end_date date NULL,
	dsl varchar(2000) NULL,
	cme_credits numeric NULL,
	completed char(1) NULL,
	"degree" varchar NULL,
	CONSTRAINT pc_prac_training_pk PRIMARY KEY (id),
	CONSTRAINT pc_prac_training_pp_prac_fk FOREIGN KEY (prac_id) REFERENCES portown.pp_prac(id)
);
