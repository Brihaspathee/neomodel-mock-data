CREATE TABLE portown.pp_prov_addr (
    prov_id    INTEGER NOT NULL,
    address_id INTEGER NOT NULL,
    CONSTRAINT pk_pp_prov_addr PRIMARY KEY (prov_id, address_id),
    CONSTRAINT fk_pp_prov_addr_prov FOREIGN KEY (prov_id) REFERENCES portown.pp_prov (id),
    CONSTRAINT fk_pp_prov_addr_addr FOREIGN KEY (address_id) REFERENCES portown.pp_addr (id)
);

