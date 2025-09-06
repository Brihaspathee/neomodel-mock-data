-- auto-generated definition
create table portown.pp_prov_type
(
    id       integer not null
        constraint pp_prov_type_pk
            primary key,
    type     varchar not null,
    category varchar not null
);

alter table portown.pp_prov_type
    owner to porticoadmin;

