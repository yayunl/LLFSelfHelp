from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from django.utils.crypto import get_random_string
from datetime import datetime as dt
from catalog.models import ServiceNote, Service, ServiceDate


class Command(BaseCommand):
    help = 'Create service note data'

    def add_arguments(self, parser):
        parser.add_argument('total', type=int, help='Indicates the number of services to be created')
        parser.add_argument('-s', '--service', type=str, help='Service name')
        parser.add_argument('-n', '--note', type=str, help='Service note content')
        parser.add_argument('-dt', '--date', type=str, help='Service date (YYYY-MM-DD)')

    def handle(self, *args, **kwargs):
        total, sn, note, sdate = kwargs.get('total'), kwargs.get('service'), kwargs.get('note'), kwargs.get('date')
        sr = Service.objects.filter(name=sn).first()
        sdt = ServiceDate.objects.filter(service_date=dt.strptime(sdate, '%Y-%m-%d')).first()
        srnote = ServiceNote(note=note,
                             service=sr,
                             service_date=sdt)
        srnote.save()
        self.stdout.write('ServiceNote record saved successfully.')

