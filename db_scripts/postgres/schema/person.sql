-- auto-generated definition
create table portown.person
(
    id   integer default nextval('person_id_seq'::regclass) not null
        constraint person_pk
            primary key,
    name varchar                                            not null,
    age  integer                                            not null
);

alter table portown.person
    owner to porticoadmin;

alter sequence portown.person_id_seq owned by portown.person.id;

