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

if os.environ.get('ENV') == 'PRODUCTION':
    SECRET_KEY = os.environ.get('SECRET_KEY')
    DEBUG = False

    ALLOWED_HOSTS = ['remace-purbeurre.herokuapp.com']

    db_from_env = dj_database_url.config(conn_max_age=500)
    DATABASES['default'].update(db_from_env)
    MIDDLEWARE.append('whitenoise.middleware.WhiteNoiseMiddleware')

    PROJECT_ROOT = os.path.join(BASE_DIR,'purbeurre')
    STATIC_ROOT = os.path.join(PROJECT_ROOT,'staticfiles')
    STATICFILES_DIRS = [
        os.path.join(PROJECT_ROOT, 'static')
    ]
    STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'