-- auto-generated definition
create table portown.pp_prov_addr
(
    id         integer not null
        constraint pp_prov_addr_pk
            primary key,
    prov_id    integer
        constraint pp_prov_addr_pp_prov_id_fk
            references portown.pp_prov,
    address_id integer
        constraint pp_prov_addr_pp_addr_id_fk
            references portown.pp_addr
);

alter table portown.pp_prov_addr
    owner to porticoadmin;

