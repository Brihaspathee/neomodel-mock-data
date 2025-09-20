-- auto-generated definition
create table portown.pp_phones
(
    id        integer not null
        constraint pp_phones_pk
            primary key,
    type      varchar not null,
    area_code varchar not null,
    exchange  varchar not null,
    number    varchar not null,
    "foreign"   varchar null,
    country_code varchar null,
    foreign_phone varchar null
);

