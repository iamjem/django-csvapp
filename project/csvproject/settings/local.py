from .base import *


DEBUG = True

TEMPLATE_DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'development',
        'USER': 'postgres',
        'PASSWORD': 'password',
        'HOST': '127.0.0.1',
        'PORT': '5432',
    }
}

INSTALLED_APPS += (
    'socketio_runserver',
)

REDIS_URL = 'redis://@localhost:6379/0'
REDIS_MAX_CONNECTION = 5

BROKER_URL = REDIS_URL
CELERY_RESULT_BACKEND='djcelery.backends.database:DatabaseBackend'
CELERY_ALWAYS_EAGER = True
