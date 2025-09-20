-- psql "postgresql://porticoadmin:password@localhost:5432/portico?options=-csearch_path%3Dportown" -f master.sql
-- Run schema scripts
\i schema/drop_tables.sql
\i centene/schema/fmg_attribute_types.sql
\i centene/schema/fmg_attribute_fields.sql
\i centene/schema/pp_net.sql
\i centene/schema/pp_net_attrib.sql
\i centene/schema/pp_net_attrib_values.sql
\i centene/schema/fmg_cities.sql
\i centene/schema/fmg_counties.sql
\i schema/create_tables.sql
\i centene/data/fmg_attribute_types.sql
\i centene/data/fmg_attribute_fields.sql
\i centene/data/pp_net.sql
\i data/insert_data.sql