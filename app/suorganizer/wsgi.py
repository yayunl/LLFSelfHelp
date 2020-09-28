"""
WSGI config for suorganizer project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/howto/deployment/wsgi/
"""

import os
from django.core.wsgi import get_wsgi_application

if int(os.environ.get('DEBUG', 1)) == 1:
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', "suorganizer.settings.dev")
else:
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', "suorganizer.settings.prod")

application = get_wsgi_application()
