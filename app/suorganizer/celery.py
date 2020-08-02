import os
from celery import Celery
from django.conf import settings


# set the default Django settings module for the 'celery' program.
if os.environ.get('ENV') == 'dev':
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', "suorganizer.settings.dev")
else:
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', "suorganizer.settings.prod")

app = Celery('suorganizer')

# Using a string here means the worker don't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)


@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))