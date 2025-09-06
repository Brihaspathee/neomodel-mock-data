-- auto-generated definition
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

alter table portown.fmg_attribute_fields
    owner to porticoadmin;

