-- delete database and user
DROP DATABASE IF EXISTS "Nutella_db";
DROP USER IF EXISTS "Nutella_user";

-- create the database for this project
CREATE DATABASE "Nutella_db";
--create the user for this project and give him the rights on the project database
CREATE USER "Nutella_user" WITH PASSWORD 'Nutella_pwd';
ALTER ROLE "Nutella_user" SET client_encoding TO "utf8"; ALTER ROLE "Nutella_user" SET default_transaction_isolation TO "read committed";
ALTER ROLE "Nutella_user" SET timezone TO "UTC";
ALTER ROLE "Nutella_user" WITH CREATEDB;
ALTER DATABASE "Nutella_db" OWNER TO "Nutella_user";
GRANT ALL PRIVILEGES ON "Nutella_db" TO "Nutella_user";
