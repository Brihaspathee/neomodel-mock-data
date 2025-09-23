CREATE TABLE portown.pp_prac_hosp (
	prac_id integer NOT NULL,
	prov_id integer NULL,
	"PRIMARY" char(1) NULL,
	privilege varchar NULL,
	"rank" varchar NULL,
	priv_exp_date date NULL,
	priv_eff_date date NULL,
	CONSTRAINT pp_prac_hosp_pp_prac_fk FOREIGN KEY (prac_id) REFERENCES portown.pp_prac(id),
	CONSTRAINT pp_prac_hosp_pp_prov_fk FOREIGN KEY (prov_id) REFERENCES portown.pp_prov(id)
);
