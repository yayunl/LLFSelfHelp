from .base import *
import os
# import django_heroku


# BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# PROJECT_ROOT = os.path.dirname(BASE_DIR)


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False
TEMPLATE_DEBUG = False
SECRET_KEY = os.environ.get('SECRET_KEY')
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')


# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': os.environ.get('SQL_ENGINE'),
        'NAME': os.environ.get('SQL_DATABASE'),
        'USER': os.environ.get('SQL_USER'),
        'PASSWORD': os.environ.get('SQL_PASSWORD'),
        'HOST': os.environ.get('SQL_HOST'),
        'PORT': os.environ.get('SQL_PORT'),
    }
}


# Celery beat
CELERY_BEAT_SCHEDULE = {
    'scheduled_services_reminders': {
        'task': 'send_service_reminders',
        'schedule': crontab(hour=9, minute=30, day_of_week='mon') # Send every Monday morning at 9:30 am
        # 'args': (10 , 20)
    },
    'scheduled_prep_reminders': {
        'task': 'send_prep_reminder',
        'schedule': crontab(hour=18, minute=30, day_of_week='mon') # Send every Monday afternoon at 6:30 am
        # 'args': (10 , 20)
    },
}


# prod_db = dj_database_url.config(conn_max_age=500)
# DATABASES['default'].update(prod_db)

###############################
# Uncommented when using Heroku
###############################

# django_heroku.settings(locals())

### END###########


# Static files



## Amazon Credentials

# AWS_STORAGE_BUCKET_NAME = os.environ.get('AWS_STORAGE_BUCKET_NAME')
# AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
# AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')

# Tell django-storages that when coming up with the URL for an item in S3 storage, keep
# it simple - just use this domain plus the path. (If this isn't set, things get complicated).
# This controls how the `staticfiles` template tag from `staticfiles` gets expanded, if you're using it.
# We also use it in the next setting.

# AWS_S3_CUSTOM_DOMAIN = '%s.s3.us-east-2.amazonaws.com' % AWS_STORAGE_BUCKET_NAME

## Gets all staticfiles files from the amazon S3 staticfiles folder

# STATICFILES_LOCATION = 'staticfiles'
# STATICFILES_STORAGE = 'custom_storages.StaticStorage'
# STATIC_URL = "https://%s/%s/" % (AWS_S3_CUSTOM_DOMAIN, STATICFILES_LOCATION)
#
