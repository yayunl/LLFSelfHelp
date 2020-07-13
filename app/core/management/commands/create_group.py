from django.core.management.base import BaseCommand
from django.utils.crypto import get_random_string
from catalog.models import Group


class Command(BaseCommand):
    help = 'Create group data'

    def add_arguments(self, parser):
        parser.add_argument('total', type=int, help='Indicates the number of groups to be created')
        parser.add_argument('-g', '--group', type=str, help='Group name')
        parser.add_argument('-ds', '--description', type=str, help='Group description')

    def handle(self, *args, **kwargs):
        total, gn, ds = kwargs.get('total'), kwargs.get('group'), kwargs.get('description')
        if not gn and not ds:
            records = list()
            for i in range(total):
                gr = Group(name=get_random_string())
                records.append(gr)
            Group.objects.bulk_create(records)
            self.stdout.write('Group records saved successfully.')
        else:
            gr = Group(name=kwargs.get('group'),
                       description=kwargs.get('description'))
            gr.save()
            self.stdout.write('Group record saved successfully.')

