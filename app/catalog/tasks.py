from celery import task
from django.template.loader import render_to_string
from django.core.mail import send_mail
from datetime import datetime as dt
import os, datetime

# project imports
from catalog.models import Service, Group
from catalog.utils import service_dates, str2date, date2str
from users.models import User
from users.utils import SERMON_GROUP


@task(name='send_coordinator_of_week_reminder')
def send_coordinator_of_week_reminder():
    """
    Send reminder to the coordinator of the week.
    :return:
    """
    sender_email = os.environ.get('EMAIL_HOST_USER')

    this_week_service_date_str, _, _, _ = service_dates()
    this_week_services_query = Service.objects.filter(service_date=str2date(this_week_service_date_str))
    # Get the service
    coord_of_week_service = Service.objects.filter(service_date=str2date(this_week_service_date_str),
                                                   categories__name='事务报告/当周主席')
    # Get fellowship coordinators' emails
    coordinator_emails = [user.email for user in User.objects.filter(is_staff=True).all()]

    # Get the email of the coordinator of the week
    servant_email = [servant.email for service in coord_of_week_service.all() for servant in service.servants.all()]
    if len(servant_email) == 0:
        return "No coordinator of the week is found."

    # Build recipients' email list
    recipients = servant_email + coordinator_emails
    unique_emails = set(recipients)
    recipient_emails_str = ';'.join(list(unique_emails))
    recipient_emails = unique_emails

    # Build email content
    context = {'services': this_week_services_query,
               'emails': recipient_emails_str,
               'subject': f'本周 ( {this_week_service_date_str} ) 团契报告提醒',
               'greetings': f"Hello, 很高兴你参与团契事务报告的服事！本周({this_week_service_date_str})服事团队如下。"
                            f"请在周四之前发送团契聚会提醒邮件，并且在周五之前准备好当周团契报告。谢谢！"}

    email_subject = render_to_string('users/reminder_email_subject.txt', context).replace('\n', '')
    email_body = render_to_string('users/reminder_email_body.txt', context)

    # print(email_subject)
    # print(email_body)
    # # Send email
    send_mail(
        email_subject,
        email_body,
        sender_email,
        recipient_emails,
        fail_silently=False,
    )

    return "Coordinator reminder email was sent."


# Send reminders of the services of the upcoming week
@task(name='send_service_reminder')
def send_service_reminder():
    """
    Send reminder to servants who have services in the week.
    :return:
    """
    sender_email = os.environ.get('EMAIL_HOST_USER')

    this_week_service_date_str, _, this_week_sunday_date_str, _ = service_dates()
    this_week_services_query = Service.objects.filter(service_date__in=[str2date(this_week_service_date_str),
                                                                        str2date(this_week_sunday_date_str)])

    # Get coordinators' emails
    coordinator_emails = [user.email for user in User.objects.filter(is_staff=True).all()]

    # Send email reminder to servants who have services in this week.
    servant_emails = list()
    for service in this_week_services_query:
        for servant in service.servants.all():
            if servant.group.name not in SERMON_GROUP: # exclude preachers
                servant_emails.append(servant.email)
    # servants = [servant.email for service in this_week_services_query.all() for servant in service.servants.all()]
    if len(servant_emails) == 0:
        return "No servants found for services of the week."

    # Build recipients' email list
    recipients = servant_emails + coordinator_emails
    unique_emails = set(recipients)
    recipient_emails_str = ';'.join(list(unique_emails))
    recipient_emails = unique_emails

    # Build email content
    context = {'services': this_week_services_query,
               'emails': recipient_emails_str,
               'subject': f'本周 ( {this_week_service_date_str} ) 团契服事提醒',
               'greetings': f"Hello, 很高兴你参与本周的团契服事！本周({this_week_service_date_str})服事团队如下:"}

    email_subject = render_to_string('users/reminder_email_subject.txt', context).replace('\n', '')
    email_body = render_to_string('users/reminder_email_body.txt', context)

    # Send email
    send_mail(
        email_subject,
        email_body,
        sender_email,
        recipient_emails,
        fail_silently=False,
    )

    return "Services reminder email sent."


@task(name='send_prep_reminder')
def send_prep_reminder():
    """
    Send the reminder to servants who are design bible study materials for the next week.
    :return:
    """
    sender_email = os.environ.get('EMAIL_HOST_USER')
    _, following_service_date_str, _, _ = service_dates()
    bible_study_prep_service = Service.objects.filter(service_date=str2date(following_service_date_str),
                                                      categories__name__in=('查经设计', '查经设计协助')).all()
    # get coordinators' emails
    coordinator_emails = [user.email for user in User.objects.filter(is_staff=True).all()]
    # Send email reminder to servants who have services in this week.
    servant_emails = [servant.email for service in bible_study_prep_service for servant in service.servants.all()]

    if len(servant_emails) == 0:
        return "No servants of the study material for the next week are found."

    recipients = servant_emails + coordinator_emails
    unique_emails = set(recipients)
    recipient_emails_str = ';'.join(list(unique_emails))
    recipient_emails = unique_emails

    # Build email content
    context = {'services': bible_study_prep_service,
               'emails': recipient_emails_str,
               'subject': f'下周 ( {following_service_date_str} ) 查经设计提醒',
               'greetings': "Hello, 很高兴你参与查经设计服事！你在下周二将会有查经设计的服事，"
                            "请和预查设计的辅导沟通并设计好预查材料。"
                            "请在下周二之前和各小组带领的同工分享设计材料。谢谢！"}

    email_subject = render_to_string('users/reminder_email_subject.txt', context).replace('\n', '')
    email_body = render_to_string('users/reminder_email_body.txt', context)

    # Send email
    send_mail(
        email_subject,
        email_body,
        sender_email,
        recipient_emails,
        fail_silently=False,
    )

    return "Prep reminder email sent."


@task(name='send_birthday_reminder')
def send_birthday_reminder():
    """
    Send birthday celebration reminder to servants who are in charge of this service.
    :return:
    """
    birthday_of_day_users = None

    sender_email = os.environ.get('EMAIL_HOST_USER')
    _, following_service_date_str, _, _ = service_dates()

    birthday_celebration_service = Service.objects.filter(categories__name='庆生').first()
    birthday_of_month_users = User.objects.filter(birthday__month=date2str(datetime.datetime.now()).split('-')[-2]).all()

    if birthday_of_month_users:
        birthday_of_day_users = [user for user in birthday_of_month_users
                                 if date2str(user.birthday).split('-')[-1] == date2str(datetime.datetime.now()).split('-')[-1]]

    if not birthday_of_day_users:
        return "No birthday of the day is found."

    # Get coordinators' emails
    # coord_emails = [user.email for user in User.objects.filter(is_staff=True).all()]

    # Get servants' emails
    servant_emails = [servant.email for servant in birthday_celebration_service.servants.all()]
    # unique_emails = set(servant_emails + coord_emails)
    unique_emails = set(servant_emails)
    recipient_emails_str = ';'.join(list(unique_emails))
    recipient_emails = unique_emails

    # Build email content
    context = {'services': birthday_celebration_service,
               'birthday_of_day_users': birthday_of_day_users,
               'emails': recipient_emails_str,
               'subject': f'今日庆生提醒',
               'greetings': "Hello, 很高兴你参与团契庆生服事！请在群里为今天过生日的成员发送生日祝福。谢谢！"}

    email_subject = render_to_string('users/reminder_email_subject.txt', context).replace('\n', '')
    email_body = render_to_string('users/reminder_email_body.txt', context)

    # print(recipient_emails)
    # print(birthday_of_day_users)
    # print(email_body)

    # Send email
    send_mail(
        email_subject,
        email_body,
        sender_email,
        recipient_emails,
        fail_silently=False,
    )

    return "Birthday of the day reminder email sent."


def send_mail_async(kwargs):
    number_sent = send_mail(**kwargs)
    return number_sent