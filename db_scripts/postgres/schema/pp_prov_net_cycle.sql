CREATE TABLE portown.pp_prov_net_cycle (
	id integer NOT NULL,
	prov_id integer NOT NULL,
	net_id numeric NOT NULL,
	status varchar NOT NULL,
	start_date date NOT NULL,
	end_date date NOT NULL,
	CONSTRAINT pp_prov_net_cycle_pk PRIMARY KEY (id),
	CONSTRAINT pp_prov_net_cycle_pp_prov_fk FOREIGN KEY (prov_id) REFERENCES portown.pp_prov(id),
	CONSTRAINT pp_prov_net_cycle_pp_net_fk FOREIGN KEY (net_id) REFERENCES portown.pp_net(id)
);