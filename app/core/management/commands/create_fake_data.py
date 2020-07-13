from django.core.management.base import BaseCommand
from catalog.models import Group, Service, ServiceNote, ServiceDate
from users.models import User
from datetime import datetime as dt


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

        # Create two services
        services = [('Bible study', 'Studying the Lords word'),
                    ('Food pickup', 'Picking up food')]
        for service in services:
            sr = Service(name=service[0],
                         description=service[1])
            sr.save()
            sd = ServiceDate(service_date=dt.strptime('2020-07-17', '%Y-%m-%d'))
            sd.save()

            sr.service_dates.add(sd)
        self.stdout.write('Service records created successfully.')

        # Create service notes
        service_notes = [('Genesis 1', '2020-07-17', 'Bible study'),
                         ('Panda Express at 6:40 pm', '2020-07-17', 'Food pickup')]
        for sn in service_notes:
            service = Service.objects.filter(name=sn[-1]).first()
            sdate = ServiceDate.objects.filter(service_date=dt.strptime(sn[1], '%Y-%m-%d')).first()
            srnote = ServiceNote(note=sn[0],
                                 service=service,
                                 service_date=sdate)
            srnote.save()
        self.stdout.write('Service notes created successfully.')

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