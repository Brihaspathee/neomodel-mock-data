-- psql "postgresql://porticoadmin:password@localhost:5432/portico?options=-csearch_path%3Dportown" -f master.sql
-- Run schema scripts
\i centene/schema/drop_tables.sql
\i centene/schema/fmg_attribute_types.sql
\i centene/schema/fmg_attribute_fields.sql
\i centene/schema/pp_net.sql
\i centene/schema/pp_net_attrib.sql
\i centene/schema/pp_net_attrib_values.sql
\i centene/schema/fmg_cities.sql
\i centene/schema/fmg_counties.sql
\i centene/schema/pp_prov_tin.sql
\i centene/schema/pp_prov_type.sql
\i centene/schema/pp_spec.sql
\i centene/schema/pp_addr.sql
\i centene/schema/pp_phones.sql
\i centene/schema/pp_prov.sql
\i centene/schema/pp_prov_addr.sql
\i centene/schema/pp_addr_phones.sql
\i centene/schema/pp_prov_tin_loc.sql
\i centene/schema/pp_prov_loc.sql
\i centene/schema/pp_prov_net_cycle.sql
\i centene/schema/pp_prov_net_loc_cycle.sql
\i centene/schema/pp_prov_attrib.sql
\i centene/schema/pp_prov_attrib_values.sql
\i centene/schema/pp_prov_loc_attrib.sql
\i centene/schema/pp_prov_loc_attrib_values.sql
-- Insert data common for all scenarios
\i centene/data/fmg_attribute_types.sql
\i centene/data/fmg_attribute_fields.sql
\i centene/data/pp_net.sql
\i centene/data/fmg_cities.sql
\i centene/data/fmg_counties.sql
\i centene/data/pp_prov_type.sql
\i centene/data/pp_spec.sql

-- Insert data for Scenario - 0
-- \i data/pp_addr.sql
-- \i data/pp_prov_tin.sql
-- \i data/pp_phones.sql
-- \i data/pp_prov.sql
-- \i data/pp_addr_phones.sql
-- \i data/pp_prov_addr.sql
-- \i data/pp_prov_attrib.sql
-- \i data/pp_prov_attrib_values.sql
-- \i data/pp_prov_tin_loc.sql
-- \i data/pp_prov_loc.sql
-- \i data/pp_prov_net_cycle.sql
-- \i data/pp_prov_net_loc_cycle.sql
-- \i data/pp_prov_loc_attrib.sql
-- \i data/pp_prov_loc_attrib_values.sql
-- \i centene/scenarios/scenario_0/scenario-data.sql

-- Insert data for Scenario - 1
\i centene/scenarios/scenario_1/provider/parent/parent_ppg.sql
