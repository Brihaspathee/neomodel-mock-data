-- auto-generated definition
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

alter table portown.pp_prov_attrib
    owner to porticoadmin;