from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from django.utils.crypto import get_random_string
from catalog.utils import date2str, str2date
from catalog.models import Service, Category


class Command(BaseCommand):
    help = 'Create service data'

    def add_arguments(self, parser):
        parser.add_argument('-c','--category', type=str, help='Service category')
        parser.add_argument('-ds', '--description', type=str, help='Service description')
        parser.add_argument('-dt', '--date', type=str, help='Service date (YYYY-MM-DD)')
        parser.add_argument('-nt', '--note', type=str, help='Note')

    def handle(self, *args, **kwargs):
        cat = Category.objects.filter(name=kwargs.get('category')).first()
        if not cat:
            cat = Category(name=kwargs.get('category'))
            cat.save()

        sr = Service(service_date=str2date(kwargs.get('date')),
                     description=kwargs.get('description'),
                     note=kwargs.get('note'))
        sr.save()
        sr.categories.add(cat)

        self.stdout.write('Service record is saved successfully.')

