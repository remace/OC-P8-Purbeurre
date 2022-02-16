from . import *

SECRET_KEY = "secret_not_secure_cause_too easy to control"
ALLOWED_HOSTS = ['127.0.0.1']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'CITestDatabase',
    }
}