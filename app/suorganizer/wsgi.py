"""
WSGI config for suorganizer project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/howto/deployment/wsgi/
"""

import os
from django.core.wsgi import get_wsgi_application

if os.environ.get('ENV').lower() == 'prod':
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', "suorganizer.settings.prod")
else:
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', "suorganizer.settings.dev")

application = get_wsgi_application()
