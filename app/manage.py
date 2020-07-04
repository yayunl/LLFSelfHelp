#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os, sys, environ

# Load env
environ.Env.read_env()
env = environ.Env(DEBUG=(bool, False),)


def main():

    if env('ENV').lower() == 'dev':
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', "suorganizer.settings.dev")
    elif env('ENV').lower() == 'prod':
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', "suorganizer.settings.prod")
    else:
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', "suorganizer.settings")

    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
