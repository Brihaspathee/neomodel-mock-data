-- 0. Create PP_NET
CREATE TABLE portown.pp_net (
	id numeric NOT NULL,
	ds varchar(100) NOT NULL,
	dsl varchar(200) NULL,
	net_level_id numeric NOT NULL,
	parent_net_id numeric NULL,
	CONSTRAINT ppnet_pk PRIMARY KEY (id)
);

-- 1. Create FMG_ATTRIBUTE_TYPES table
create table portown.fmg_attribute_types
(
    id          integer not null
        constraint fmg_attribute_types_pk
            primary key,
    metatype    varchar not null,
    description varchar
);

-- alter table portown.fmg_attribute_types
--     owner to porticoadmin;

-- 2. Create FMG_ATTRIBUTE_FIELDS table
create table portown.fmg_attribute_fields
(
    id           integer not null
        constraint fmg_attribute_fields_pk
            primary key,
    attribute_id integer not null
        constraint fmg_attribute_fields_fmg_attribute_types_id_fk
            references portown.fmg_attribute_types,
    fmgcode      varchar,
    field_name   varchar not null,
    datatype     varchar not null
);

-- 2.1 Create FMG Cities
CREATE TABLE portown.fmg_cities (
	id integer NOT NULL,
	ds varchar NOT NULL,
	CONSTRAINT fmg_cities_pk PRIMARY KEY (id)
);

-- 2.2 Create FMG Counties
    -- portown.fmg_counties definition

CREATE TABLE portown.fmg_counties (
	id int4 NOT NULL,
	ds varchar NOT NULL,
	CONSTRAINT fmg_counties_pk PRIMARY KEY (id)
);

-- alter table portown.fmg_attribute_fields
--     owner to porticoadmin;

-- 3. Create PP_PROV_TIN table
create table portown.pp_prov_tin
(
    id   integer not null
        constraint pp_prov_tin_pk
            primary key,
    name varchar not null,
    tin  varchar not null
);

-- alter table portown.pp_prov_tin
--     owner to porticoadmin;


-- 4. Create PP_PROV_TYPE table
create table portown.pp_prov_type
(
    id       integer not null
        constraint pp_prov_type_pk
            primary key,
    type     varchar not null,
    category varchar not null
);

-- alter table portown.pp_prov_type
--     owner to porticoadmin;

-- 5. Create PP_SPEC table
create table portown.pp_spec
(
    id             integer not null
        constraint pp_spec_pk
            primary key,
    type           varchar not null,
    description    varchar not null,
    site_visit_req varchar not null
);

-- alter table portown.pp_spec
--     owner to porticoadmin;

-- 6. Create PP_ADDR table
-- portown.pp_addr definition

CREATE TABLE portown.pp_addr (
	id int4 NOT NULL,
	"type" varchar NULL,
	addr1 varchar NOT NULL,
	addr2 varchar NULL,
	state varchar NOT NULL,
    addr3 varchar NULL,
	city_id int4 NOT NULL,
	county_id int4 NOT NULL,
    fips varchar NULL,
	zip varchar NOT NULL,
	latitude varchar NULL,
	longitude varchar NULL,
	start_date date NULL,
	end_date date NULL,
	CONSTRAINT id PRIMARY KEY (id)
);


-- portown.pp_addr foreign keys

ALTER TABLE portown.pp_addr ADD CONSTRAINT pp_addr_fmg_cities_fk FOREIGN KEY (city_id) REFERENCES portown.fmg_cities(id);
ALTER TABLE portown.pp_addr ADD CONSTRAINT pp_addr_fmg_counties_fk FOREIGN KEY (county_id) REFERENCES portown.fmg_counties(id);

-- alter table portown.pp_addr
--     owner to porticoadmin;

-- 6.5. Create PP_PROV_TIN_LOC
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

-- 7. Create PP_PHONES table
create table portown.pp_phones
(
    id        integer not null
        constraint pp_phones_pk
            primary key,
    type      varchar not null,
    area_code varchar not null,
    exchange  varchar not null,
    number    varchar not null
);

-- alter table portown.pp_phones
--     owner to porticoadmin;

-- 8. Create PP_PROV table
-- portown.pp_prov definition


CREATE TABLE portown.pp_prov (
	id int4 NOT NULL,
	"name" varchar NOT NULL,
	tin_id int4 NOT NULL,
	prov_type_id int4 NOT NULL,
	address_id int4 NOT NULL,
	spec_id int4 NOT NULL,
	sub_prov_code varchar NULL,
	name_usage varchar NULL,
	medicare_no varchar NULL,
	label_cluster_id varchar NULL,
	CONSTRAINT pp_prov_pk PRIMARY KEY (id)
);


-- portown.pp_prov foreign keys

ALTER TABLE portown.pp_prov ADD CONSTRAINT pp_prov_pp_addr_id_fk FOREIGN KEY (address_id) REFERENCES portown.pp_addr(id);
ALTER TABLE portown.pp_prov ADD CONSTRAINT pp_prov_pp_prov_tin_id_fk FOREIGN KEY (tin_id) REFERENCES portown.pp_prov_tin(id);
ALTER TABLE portown.pp_prov ADD CONSTRAINT pp_prov_pp_prov_type_id_fk FOREIGN KEY (prov_type_id) REFERENCES portown.pp_prov_type(id);
ALTER TABLE portown.pp_prov ADD CONSTRAINT pp_prov_pp_spec_id_fk FOREIGN KEY (spec_id) REFERENCES portown.pp_spec(id);

-- alter table portown.pp_prov
--     owner to porticoadmin;

-- 9. Create PP_ADDR_PHONES table
create table portown.pp_addr_phones
(
    id         integer not null
        constraint pp_addr_phones_pk
            primary key,
    address_id integer
        constraint pp_addr_phones_pp_addr_id_fk
            references portown.pp_addr,
    phone_id   integer
        constraint pp_addr_phones_pp_phones_id_fk
            references portown.pp_phones
);

-- alter table portown.pp_addr_phones
--     owner to porticoadmin;

-- 10. Create PP_PROV_ADDR table
CREATE TABLE portown.pp_prov_addr (
    prov_id    INTEGER NOT NULL,
    address_id INTEGER NOT NULL,
    CONSTRAINT pk_pp_prov_addr PRIMARY KEY (prov_id, address_id),
    CONSTRAINT fk_pp_prov_addr_prov FOREIGN KEY (prov_id) REFERENCES portown.pp_prov (id),
    CONSTRAINT fk_pp_prov_addr_addr FOREIGN KEY (address_id) REFERENCES portown.pp_addr (id)
);


-- 11. Create PP_PROV_ATTRIB table
create table portown.pp_prov_attrib
(
    id           integer not null
        constraint pp_prov_attrib_pk
            primary key,
    prov_id      integer
        constraint pp_prov_attrib_pp_prov_id_fk
            references portown.pp_prov,
    attribute_id integer
        constraint pp_prov_attrib_fmg_attribute_types_id_fk
            references portown.fmg_attribute_types
);

-- alter table portown.pp_prov_attrib
--     owner to porticoadmin;

-- 12. Create PP_PROV_ATTRIB_VALUES table
create table portown.pp_prov_attrib_values
(
    id                integer not null
        constraint pp_prov_attrib_values_pk
            primary key,
    prov_attribute_id integer
        constraint pp_prov_attrib_values_pp_prov_attrib_id_fk
            references portown.pp_prov_attrib,
    field_id          integer
        constraint pp_prov_attrib_values_fmg_attribute_fields_id_fk
            references portown.fmg_attribute_fields,
    value             varchar,
    value_date        date,
    value_number      numeric
);

-- alter table portown.pp_prov_attrib_values
--     owner to porticoadmin;

-- 13. Create PP_PROV_LOC table
CREATE TABLE portown.pp_prov_loc (
	prov_id integer NOT NULL,
	loc_id integer NOT NULL,
	name_usage char(1) NULL,
	"primary" char(1) NULL,
	start_date date NULL,
	end_date date NULL,
	print_supress char(1) NULL,
	CONSTRAINT pp_prov_loc_pp_prov_fk FOREIGN KEY (prov_id) REFERENCES portown.pp_prov(id),
	CONSTRAINT pp_prov_loc_pp_prov_tin_loc_fk FOREIGN KEY (loc_id) REFERENCES portown.pp_prov_tin_loc(id)
);

-- 13. Create PP_PROV_NET_CYCLE table

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

-- 13. Create PP_PROV_NET_LOC_CYCLE table

CREATE TABLE portown.pp_prov_net_loc_cycle (
	id integer NOT NULL,
	prov_net_cycle_id integer NOT NULL,
	prov_id integer NOT NULL,
	loc_id integer NOT NULL,
	start_date date NOT NULL,
	end_date date NOT NULL,
	"primary" char(1) NOT NULL,
	CONSTRAINT pp_prov_net_loc_cycle_pk PRIMARY KEY (id),
	CONSTRAINT pp_prov_net_loc_cycle_pp_prov_net_cycle_fk FOREIGN KEY (prov_net_cycle_id) REFERENCES portown.pp_prov_net_cycle(id),
	CONSTRAINT pp_prov_net_loc_cycle_pp_prov_fk FOREIGN KEY (prov_id) REFERENCES portown.pp_prov(id),
	CONSTRAINT pp_prov_net_loc_cycle_pp_prov_tin_loc_fk FOREIGN KEY (loc_id) REFERENCES portown.pp_prov_tin_loc(id)
);

-- 14. Create PP_PROV_LOC_ATTRIB table
CREATE TABLE portown.pp_prov_loc_attrib (
	id numeric NOT NULL,
	prov_id integer NOT NULL,
	loc_id numeric NOT NULL,
	attribute_id integer NOT NULL,
	CONSTRAINT pp_prov_loc_attrib_pk PRIMARY KEY (id),
	CONSTRAINT pp_prov_loc_attrib_pp_prov_fk FOREIGN KEY (prov_id) REFERENCES portown.pp_prov(id),
	CONSTRAINT pp_prov_loc_attrib_pp_prov_tin_loc_fk FOREIGN KEY (loc_id) REFERENCES portown.pp_prov_tin_loc(id),
	CONSTRAINT pp_prov_loc_attrib_fmg_attribute_types_fk FOREIGN KEY (attribute_id) REFERENCES portown.fmg_attribute_types(id)
);

-- 15. Create PP_PROV_LOC_ATTRIB_VALUES table
CREATE TABLE portown.pp_prov_loc_attrib_values (
	id varchar NOT NULL,
	prov_loc_attribute_id numeric NOT NULL,
	field_id integer NOT NULL,
	value varchar NULL,
	value_date date NULL,
	value_number numeric NULL,
	CONSTRAINT pp_prov_loc_attrib_values_pk PRIMARY KEY (id),
	CONSTRAINT pp_prov_loc_attrib_values_pp_prov_loc_attrib_fk FOREIGN KEY (prov_loc_attribute_id) REFERENCES portown.pp_prov_loc_attrib(id),
	CONSTRAINT pp_prov_loc_attrib_values_fmg_attribute_fields_fk FOREIGN KEY (field_id) REFERENCES portown.fmg_attribute_fields(id)
);


