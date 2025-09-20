-- auto-generated definition
create table portown.pp_addr_phones
(
    address_id integer
        constraint pp_addr_phones_pp_addr_id_fk
            references portown.pp_addr,
    phone_id   integer
        constraint pp_addr_phones_pp_phones_id_fk
            references portown.pp_phones
);

