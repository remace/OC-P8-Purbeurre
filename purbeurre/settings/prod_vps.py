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

ALLOWED_HOSTS = ['127.0.0.1']


sentry_sdk.init(
    dsn="https://fe7c562ac6d5471bb4939189a4a638d6@o1137137.ingest.sentry.io/6214265",
    integrations=[DjangoIntegration()],
    traces_sample_rate=1.0,
    send_default_pii=True
)