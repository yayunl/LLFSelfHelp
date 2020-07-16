from django.core.management.base import BaseCommand
from catalog.models import Group, Service, Category
from users.models import User
from datetime import datetime as dt
from catalog.utils import str2date

class Command(BaseCommand):
    help = 'Create fake data'

    # def add_arguments(self, parser):
    #     parser.add_argument('total', type=int, help='Indicates the number of groups to be created')
    #     parser.add_argument('-g', '--group', type=str, help='Group name')
    #     parser.add_argument('-ds', '--description', type=str, help='Group description')

    def handle(self, *args, **kwargs):
        # Create two groups
        group_names = [('Xiyangyang', 'Little Lamb Group'), ('Aijiabei', 'Agape Group')]
        for group in group_names:
            gr = Group(name=group[0], description=group[1])
            gr.save()
        self.stdout.write('Group records saved successfully.')

        # Create two categories
        cts = [('Bible study', 'Studying the Lords word'),
               ('Food pickup', 'Picking up food')]
        for c in cts:
            cat = Category(name=c[0], description=c[1])
            cat.save()

        # Create two services
        categories = Category.objects.filter().all()
        c1, c2 = categories[0], categories[1]
        services = [(c1, 'Genesis1', str2date('2020-07-18'), 'Nothing' ),
                    (c2, 'Panda', str2date('2020-07-17'),'Picking up food')]

        for service in services:
            sr = Service(category=service[0],
                         description=service[1],
                         service_date=service[2],
                         note=service[-1])
            sr.save()
        self.stdout.write('Service records created successfully.')

        # Create four fake members
        # grp1 = Group.objects.filter(name='Xiyangyang').first()
        # grp2 = Group.objects.filter(name='Aijiabei').first()
        users = [('user1', 'password', 'user1@gmail.com', 'USER_1'), # username, password, email, name, group_id
                 ('user2', 'password', 'user2@gmail.com', 'USER_2'),
                 ('user3', 'password', 'user3@gmail.com', 'USER_3'),
                 ('user4', 'password', 'user4@gmail.com', 'USER_4')]

        records = list()
        for user in users:
            usr = User(username=user[0],
                       email=user[2],
                       name=user[3])
            # User model uses `set_password` to hash the password
            usr.set_password(user[1])
            # records.append(usr)
            usr.save()
        self.stdout.write('User records created successfully.')