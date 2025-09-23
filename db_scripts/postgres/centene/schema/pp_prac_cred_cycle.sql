CREATE TABLE portown.pp_prac_cred_cycle (
	id integer NOT NULL,
	prac_id integer NOT NULL,
	cred_type varchar NOT NULL,
	start_date date NOT NULL,
	end_date date NOT NULL,
	committee_date date NULL,
	status varchar NULL,
	credentialer integer NULL,
	is_delegated_cred char(1) NULL,
	affiliated_agency varchar NULL,
	recruited_by integer NULL,
	note varchar(4000) NULL,
	CONSTRAINT pp_prac_cred_cycle_pk PRIMARY KEY (id),
	CONSTRAINT pp_prac_cred_cycle_pp_prac_fk FOREIGN KEY (prac_id) REFERENCES portown.pp_prac(id)
);
