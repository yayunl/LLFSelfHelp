from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from django.utils.crypto import get_random_string
from datetime import datetime as dt
from catalog.models import Service, ServiceDate, ServiceNote


class Command(BaseCommand):
    help = 'Create service data'

    def add_arguments(self, parser):
        # parser.add_argument('services', type=int, help='Indicates the number of users to be created')

        parser.add_argument('-s', '--service', type=str, help='Service name')
        parser.add_argument('-ds', '--description', type=str, help='Service description')
        parser.add_argument('-dt', '--date', type=str, help='Service date (YYYY-MM-DD)')

    def handle(self, *args, **kwargs):
        sr = Service(name=kwargs.get('service'), description=kwargs.get('description'))
        sr.save()
        sd = ServiceDate(service_date=dt.strptime(kwargs.get('date'), '%Y-%m-%d'))
        sd.save()

        sr.service_dates.add(sd)

        self.stdout.write('Service record is saved successfully.')

