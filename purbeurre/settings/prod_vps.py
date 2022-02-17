import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration
from . import *

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

SECRET_KEY = os.environ.get('SECRET_KEY')
DEBUG = False
ALLOWED_HOSTS = ['127.0.0.1'] # à modifier une fois sur le serveur


# static files
PROJECT_ROOT = BASE_DIR
STATIC_ROOT = os.path.join(BASE_DIR,'staticfiles')
STATICFILES_DIRS = [
        os.path.join(PROJECT_ROOT, 'static')
    ]

# sentry sdk
sentry_sdk.init(
    dsn="", # à modifier selon le serveur
    integrations=[DjangoIntegration()],
    traces_sample_rate=1.0,
    send_default_pii=True
)