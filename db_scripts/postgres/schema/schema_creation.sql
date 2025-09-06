-- Run the following SQL command to create a separate database:
-- Login to postgres db using root user(postgres) and password(cognizant)
CREATE DATABASE portico;

-- use postgres root username and password and connect to the artemis_gatewaydb and run the following commands

-- Create a new user specifically for this database:

CREATE USER porticoadmin WITH PASSWORD 'password';

-- Grant the user permissions to the database:
GRANT ALL PRIVILEGES ON DATABASE portico TO porticoadmin;

-- Login to portico using the username porticoadmin and password and execute the following commands

-- Create a schema for organizing tables:
CREATE SCHEMA PORTOWN AUTHORIZATION porticoadmin;

-- Set the default schema for the user:
ALTER ROLE porticoadmin SET search_path TO PORTOWN;