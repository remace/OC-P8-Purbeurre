CREATE DATABASE 'Nutella_db';
CREATE USER 'Nutella_db' WITH PASSWORD 'Nutella_pwd';
ALTER ROLE 'Nutella_user' SET client_encoding TO 'utf8'; ALTER ROLE 'Nutella_user' SET default_transaction_isolation TO 'read committed';
ALTER ROLE 'Nutella_user' SET timezone TO 'UTC';
ALTER ROLE 'Nutella_user' WITH CREATEDB;
GRANT ALL PRIVILEGES ON 'Nutella_db' TO 'Nutella_user'