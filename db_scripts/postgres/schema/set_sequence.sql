-- Create a sequence if it doesn't exist
CREATE SEQUENCE portown.person_id_seq;

-- Alter the table to use it as a default
ALTER TABLE portown.person
ALTER COLUMN id SET DEFAULT nextval('portown.person_id_seq');

-- Optionally set ownership to manage lifecycle
ALTER SEQUENCE portown.person_id_seq OWNED BY portown.person.id;

-- Fix the sequence's current value to avoid conflicts
SELECT setval('portown.person_id_seq', (SELECT MAX(id) FROM portown.person));

