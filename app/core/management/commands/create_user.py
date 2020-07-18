from django.core.management.base import BaseCommand
from django.utils.crypto import get_random_string
from datetime import datetime as dt
from users.models import User
from catalog.models import Group


class Command(BaseCommand):
    help = 'Create user data'

    def add_arguments(self, parser):
        parser.add_argument('total', type=int, help='Indicates the number of members to be created')
        parser.add_argument('-u', '--username', type=str, help='Username')
        parser.add_argument('-e', '--email', type=str, help='Email address')
        parser.add_argument('-pwd', '--password', type=str, help='Password')
        parser.add_argument('-n', '--name', type=str, help='Name')

    def handle(self, *args, **kwargs):
        total, un, email, password, name = kwargs.get('total'), kwargs.get('username'), \
                                           kwargs.get('email'), kwargs.get('password'), kwargs.get('name')

        grp = Group.objects.get(id=1)

        if not un and not email and not password and not name:
            records = list()
            for i in range(total):
                username = 'user%s'%str(i)
                name = 'User%s'%str(i)
                usr = User(username=username,
                           email=username+'@gmail.com',
                           name=name)
                # User model uses `set_password` to hash the password
                usr.set_password('password')
                usr.save()
            #     records.append(usr)
            # User.objects.bulk_create(records)
            self.stdout.write('User records saved successfully.')
        else:
            usr = User(username=un,
                       email=email,
                       name=name,
                       group=grp)
            usr.set_password(password)
            usr.save()
            self.stdout.write('User record saved successfully.')

