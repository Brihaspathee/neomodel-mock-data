-- portown.pp_prac_loc definition

-- Drop table

-- DROP TABLE portown.pp_prac_loc;

CREATE TABLE portown.pp_prac_loc (
	prac_id int4 NOT NULL,
	prov_id int4 NOT NULL,
	loc_id int4 NOT NULL,
	"PRIMARY" bpchar(1) NULL,
	print_suppress bpchar(1) NULL,
	start_date date NULL,
	end_date date NULL,
	label_cluster_id numeric NULL
);


-- portown.pp_prac_loc foreign keys

ALTER TABLE portown.pp_prac_loc ADD CONSTRAINT pp_prac_loc_pp_prac_fk FOREIGN KEY (prac_id) REFERENCES portown.pp_prac(id);
ALTER TABLE portown.pp_prac_loc ADD CONSTRAINT pp_prac_loc_pp_prov_fk FOREIGN KEY (prov_id) REFERENCES portown.pp_prov(id);
ALTER TABLE portown.pp_prac_loc ADD CONSTRAINT pp_prac_loc_pp_prov_tin_loc_fk FOREIGN KEY (loc_id) REFERENCES portown.pp_prov_tin_loc(id);