-- auto-generated definition
create table portown.pp_prov_tin
(
    id   integer not null
        constraint pp_prov_tin_pk
            primary key,
    name varchar not null,
    tin  varchar not null
);

alter table portown.pp_prov_tin
    owner to porticoadmin;

