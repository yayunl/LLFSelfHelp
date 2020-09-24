from .base import *
import os

# BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# SECURITY WARNING: keep the secret key used in production secret!
DEBUG = True
TEMPLATE_DEBUG = True
SECRET_KEY = os.environ.get('SECRET_KEY')
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')



# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': os.environ.get('SQL_ENGINE', 'django.db.backends.sqlite3'),
        'NAME': os.environ.get('SQL_DATABASE', os.path.join(BASE_DIR, 'db.sqlite3')),
        'USER':  os.environ.get('SQL_USER', 'user'),
        'PASSWORD': os.environ.get('SQL_PASSWORD', 'password'),
        'HOST':  os.environ.get('SQL_HOST', 'localhost'),
        'PORT': os.environ.get('SQL_PORT', '5432'),
    }
}


# Caches
# https://docs.djangoproject.com/en/1.8/topics/cache/#local-memory-caching

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
    }
}
CACHE_MIDDLEWARE_ALIAS = 'default'


# Celery beat
CELERY_BEAT_SCHEDULE = {
    'scheduled_services_reminders': {
        'task': 'send_service_reminders',
        'schedule': crontab(hour=22, minute=50, day_of_week='mon') # Send every Monday  at 10:50 pm
        # 'args': (10 , 20)
    },
    'scheduled_prep_reminders': {
        'task': 'send_prep_reminder',
        'schedule': crontab(hour=23, minute=30, day_of_week='mon') # Send every Monday  at 11:30 pm
    },
    'scheduled_birthday_reminders': {
        'task': 'send_birthday_reminder',
        'schedule': crontab(hour=7, minute=30, day_of_week='mon-sun') # Send every day at 7:30 am
    },
}

