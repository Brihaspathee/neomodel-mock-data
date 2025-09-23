CREATE TABLE portown.pp_prac_addr (
	prac_id integer NOT NULL,
	address_id integer NOT NULL,
	CONSTRAINT pp_prac_addr_pp_addr_fk FOREIGN KEY (address_id) REFERENCES portown.pp_addr(id),
	CONSTRAINT pp_prac_addr_pp_prac_fk FOREIGN KEY (prac_id) REFERENCES portown.pp_prac(id)
);
