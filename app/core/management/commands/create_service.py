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
        services = [('查经', 'Bible Study', '创世纪1', '2020-07-20'),
                    ('查经', 'Bible Study', '创世纪2', '2020-07-25'),
                    ('查经', 'Bible Study', '创世纪3', '2020-07-31'),
                    ('敬拜', 'Worship', '新心音乐', '2020-07-20'),
                    ('敬拜', 'Worship', '赞美之泉', '2020-07-25'),
                    ('敬拜', 'Worship', 'Hillsong', '2020-07-31'),
                    ('饭食', 'Food pickup', 'First Chinese', '2020-07-20'),
                    ('饭食', 'Food pickup', 'Panda Express', '2020-07-25'),
                    ('饭食', 'Food pickup', 'Chickfila', '2020-07-31'),
                    ]

        kcat, kds, kdt, knt = kwargs.get('category'), kwargs.get('description'), kwargs.get('date'), kwargs.get('note')
        # Create several services
        if not kcat and not kds and not kdt and not knt:
            for ser in services:
                cat = Category.objects.filter(name=ser[0]).first()
                if not cat:
                    # Create the category
                    cat = Category(name=ser[0])
                    cat.save()

                s = Service(description=ser[1],
                            note=ser[2],
                            service_date=str2date(ser[-1]),
                            )
                s.save()
                s.categories.add(cat)
            # todo: create services of the week

            self.stdout.write('Service records are saved successfully.')

        else: # Create a service
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

