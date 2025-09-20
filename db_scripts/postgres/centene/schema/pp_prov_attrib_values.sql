-- auto-generated definition
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
            references portown.fmg_attrib_fields,
    value             varchar,
    value_date        date,
    value_number      numeric,
    LABEL_CLUSTER_ID  numeric
);

alter table portown.pp_prov_attrib_values
    owner to porticoadmin;

