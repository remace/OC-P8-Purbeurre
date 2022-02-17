from . import *

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "secret_not_secure_cause_too easy to control"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
ALLOWED_HOSTS = ['127.0.0.1']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'Nutella_db',
        'USER': 'Nutella_user',
        'PASSWORD': 'Nutella_pwd',
        'HOST': 'localhost',
        'PORT': '5432',
        'TEST': {
            'NAME': 'test_database',
        }
    }
}

PROJECT_ROOT = BASE_DIR
STATIC_ROOT = os.path.join(BASE_DIR,'staticfiles')