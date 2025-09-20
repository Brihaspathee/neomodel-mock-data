CREATE TABLE portown.pp_prov_net_loc_cycle (
	id integer NOT NULL,
	prov_net_cycle_id integer NOT NULL,
	prov_id integer NOT NULL,
	loc_id integer NOT NULL,
	start_date date NOT NULL,
	end_date date NOT NULL,
	"primary" char(1) NOT NULL,
    label_cluster_id numeric NULL,
	CONSTRAINT pp_prov_net_loc_cycle_pk PRIMARY KEY (id),
	CONSTRAINT pp_prov_net_loc_cycle_pp_prov_net_cycle_fk FOREIGN KEY (prov_net_cycle_id) REFERENCES portown.pp_prov_net_cycle(id),
	CONSTRAINT pp_prov_net_loc_cycle_pp_prov_fk FOREIGN KEY (prov_id) REFERENCES portown.pp_prov(id),
	CONSTRAINT pp_prov_net_loc_cycle_pp_prov_tin_loc_fk FOREIGN KEY (loc_id) REFERENCES portown.pp_prov_tin_loc(id)
);
