CREATE TABLE portown.pc_prac_insurance (
	id integer NOT NULL,
	prac_id integer NOT NULL,
	carrier varchar NULL,
	"policy" varchar NULL,
	expires date NULL,
	coverage varchar NULL,
	effective date NULL,
	coverage_type varchar NULL,
	coverage_unlimited char(1) NULL,
	orig_effective_date date NULL,
	CONSTRAINT pc_prac_insurance_pk PRIMARY KEY (id),
	CONSTRAINT pc_prac_insurance_pp_prac_fk FOREIGN KEY (id) REFERENCES portown.pp_prac(id)
);
