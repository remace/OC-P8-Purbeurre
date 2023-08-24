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
postgres$> psql -f prepare_database.sql
```

then make database migrations
```
$> ./manage.py makemigrations
$> ./manage.py migrate
```

## testing the app
download geckodriver (firefox driver for selenium) and add his path to PATH. if your OS is linux-based, add a symlink to it in /usr/bin/geckodriver.
then run the functionnal test from the root of the project, virtual environment activated:
```
./manage.py test tests
```
### play with the application in localhost
at the root of the project, virtual environment activated:
``` 
./manage.py populate 5 10
./manage.py runserver
```
then go to 127.0.0.1:8000 in your web browser

## useful links

* live website -> [http://remace-purbeurre.tech](http://remace-purbeurre.tech)
