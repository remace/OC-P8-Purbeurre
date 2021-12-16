# OC-P8-Purbeurre

**version 0.1**

studies project on Django web application, agile method, unit testing, versionning.

## Awaited Functionnalities and Constraints
* search for healthier food substitutes in a postgresql database
* possibility to save a product as a favourite for the user
* requests not done with ajax
* responsive GUI
* User registration with mail and password

## developer's manual
### Setup environment
clone this repository
then, using python <= 3.9 
``` 
$> python3.9 -m venv env
$> source env/bin/activate
$> python -m pip install -r reqLinux.txt	
```

### Setup database
install postgresql database on your computer, then:
```
user$> sudo -iu postgres
postgres$> initdb --locale $lang -E UTF8 -D '/var/lib/postgres/data/'
postgres$> exit
user$> sudo systemctl enable --now postgresql.service
user$> sudo su - postgres
```
create a postgresql user with the same name as your system user, with superuser rights.
```
CREATE USER <<your_system_username>> SUPERUSER;
```

then execute this command to prepare a database for the project

```
psql -h localhost -p 5432 -d postgres -f prepare_database.sql
```

then make database migrations
```
$> ./manage.py makemigrations
$> ./manage.py migrate
```

## testing the app
### unit tests
at the root of the project, virtual environment activated:
```
./manage.py test
```
code coverage report can be seen in htmlcov/index.html
You can run code coverage with this command:
```
(env)> pip install coverage
(env)> coverage run --source "accounts,products" manage.py test -v 2 && coverage report && coverage html
```

### play with the application in localhost
at the root of the project, virtual environment activated to populate up to 5 products in 10 categories in database :
``` 
./manage.py populate 5 10
./manage.py runserver
```
then go to 127.0.0.1:8000 in your web browser

## useful links

* live website -> [https://remace-purbeurre.herokuapp.com](https://remace-purbeurre.herokuapp.com)
