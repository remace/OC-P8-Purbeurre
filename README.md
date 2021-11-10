# OC-P8-Purbeurre

**version 0.1**

studies project on Django web application, agile method, unit testing, versionning.

## Awaited Functionnalities and Constraints
* search for food products in a postgresql database
* possibility to save a product as a favourite for the user
* requests not done with ajax
* responsive GUI
* User registration with mail and password

## developer's manual
### Setup environment
clone this repository
then, using python 3.9 (3.10 has problems with psycopg2)
``` 
$> python3.9 -m venv env
$> source env/bin/activate
$> python -m pip install -r reqLinux.txt
$> ./manage.py makemigrations
$> ./manage.py migrate
	
```

### Setup database
install postgresql database on your computer, then:
```
user$> sudo -iu postgres
postgres$> initdb --locale $lang -E UTF8 -D '/var/lib/postgres/data/'
postgres$> exit
user$> sudo systemctl enable --now postgresql.service
user$> sudo su - postgres
postgres$> psql
psql#> CREATE DATABASE 'Nutella_db';
psql#> CREATE USER 'Nutella_db' WITH PASSWORD 'Nutella_pwd';
psql#> ALTER ROLE 'Nutella_user' SET client_encoding TO 'utf8'; ALTER ROLE 'Nutella_user' SET default_transaction_isolation TO 'read committed';
ALTER ROLE 'Nutella_user' SET timezone TO 'UTC';
ALTER ROLE 'Nutella_user' WITH CREATEDB;
psql#>GRANT ALL PRIVILEGES ON 'Nutella_db' TO 'Nutella_user'
psql#> \q
postgres $>exit
```

## testing the app
### unit tests
at the root of the project, virtual environment activated:
```
./manage.py test
```
### play with the application in localhost
at the root of the project, virtual environment activated:
``` 
./manage.py populate 5 10
./manage.py runserver
```
then go to 127.0.0.1:8000 in your web browser

## useful links

* [project order](https://openclassrooms.com/fr/paths/68/projects/159/assignment)
* [Trello](https://trello.com/invite/b/MMPgH3xg/30eb1dde28f68f9aec60cc5e2eb01925/p8-openfoodfacts)
* live website -> still not posted
* document on conception process -> still not posted
