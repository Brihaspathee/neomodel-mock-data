-- auto-generated definition
create table portown.pp_addr
(
    id         integer not null
        constraint id
            primary key,
    type       varchar,
    addr1      varchar not null,
    addr2      varchar,
    city       varchar not null,
    state      varchar not null,
    zip        varchar not null,
    county     varchar,
    latitude   varchar,
    longitude  varchar,
    start_date date,
    end_date   date,
    fips       varchar
);

comment on column portown.pp_addr.id is 'Primary key of the table';

comment on constraint id on portown.pp_addr is 'The primary key of the table';

comment on column portown.pp_addr.type is 'Type of the address';

comment on column portown.pp_addr.addr1 is 'Address line 1';

comment on column portown.pp_addr.addr2 is 'Address line 2';

comment on column portown.pp_addr.city is 'City of the address';

comment on column portown.pp_addr.state is 'State of the address';

comment on column portown.pp_addr.zip is 'Zip code of the address';

comment on column portown.pp_addr.county is 'County of the address';

comment on column portown.pp_addr.latitude is 'Latitude of the address';

comment on column portown.pp_addr.longitude is 'Longitude of the address';

comment on column portown.pp_addr.start_date is 'Start date of the address';

comment on column portown.pp_addr.end_date is 'End date of the address';

comment on column portown.pp_addr.fips is 'FIPS Code of the county';

alter table portown.pp_addr
    owner to porticoadmin;

