CREATE TABLE portown.pp_prov_tin_loc (
	id numeric NOT NULL,
	tin_id numeric NULL,
	address_id integer NOT NULL,
	"name" varchar(100) NOT NULL,
	"primary" char(1) NULL,
	print_suppress char(1) NULL,
	office_mgr varchar(100) NULL,
	train char(1) NULL,
	bus char(1) NULL,
	transit_route varchar(100) NULL,
	handicap varchar(100) NULL,
	prov_tin_prc_cont_id numeric NULL,
	CONSTRAINT pp_prov_tin_loc_pk PRIMARY KEY (id),
	CONSTRAINT pp_prov_tin_loc_pp_addr_fk FOREIGN KEY (address_id) REFERENCES portown.pp_addr(id)
);