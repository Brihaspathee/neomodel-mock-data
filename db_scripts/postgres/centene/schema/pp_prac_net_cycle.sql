CREATE TABLE portown.pp_prac_net_cycle (
	id integer NOT NULL,
	prac_id integer NOT NULL,
	net_id integer NOT NULL,
	start_date date NULL,
	end_date date NULL,
	status varchar NULL,
	label_cluster_id numeric NULL,
	CONSTRAINT pp_prac_net_cycle_pk PRIMARY KEY (id),
	CONSTRAINT pp_prac_net_cycle_pp_net_fk FOREIGN KEY (net_id) REFERENCES portown.pp_net(id),
	CONSTRAINT pp_prac_net_cycle_pp_prac_fk FOREIGN KEY (prac_id) REFERENCES portown.pp_prac(id)
);
