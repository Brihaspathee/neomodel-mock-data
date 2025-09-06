CREATE TABLE portown.pp_net (
	id numeric NOT NULL,
	ds varchar(100) NOT NULL,
	dsl varchar(200) NULL,
	net_level_id numeric NOT NULL,
	parent_net_id numeric NULL,
	CONSTRAINT ppnet_pk PRIMARY KEY (id)
);