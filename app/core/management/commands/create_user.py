from django.core.management.base import BaseCommand
from django.utils.crypto import get_random_string
from django.template.defaultfilters import slugify
from users.models import User, Profile
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
                rdstr = get_random_string(5)
                username = 'user%s'%str(i) + rdstr
                name = 'User%s'%str(i)  + rdstr
                usr = User.objects.create(username=username,
                                          email=username+'@gmail.com',
                                          name=name)
                # User model uses `set_password` to hash the password
                usr.set_password('password')
                usr.save()
                # update profile
                Profile.objects.update_or_create(
                    user=usr,
                    defaults={
                        'slug': slugify(usr.get_name()),
                    }
                )
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

            Profile.objects.update_or_create(
                user=usr,
                defaults={
                    'slug': slugify(usr.get_name()),
                }
            )

            self.stdout.write('User record saved successfully.')

