-- auto-generated definition
create table portown.pp_phones
(
    id        integer not null
        constraint pp_phones_pk
            primary key,
    type      varchar not null,
    areacode varchar not null,
    exchange  varchar not null,
    num    varchar not null,
    extension    varchar null,
    "FOREIGN"   varchar null,
    country_code varchar null,
    foreign_phone varchar null
);
