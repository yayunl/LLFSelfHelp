from celery import task
from django.template.loader import render_to_string
from django.core.mail import send_mail
import os
# project imports
from catalog.models import Service
from catalog.utils import service_dates, str2date


@task(name='send_reminders')
def send_reminders():
    sender_email = os.environ.get('EMAIL_HOST_USER')
    recipient_emails = os.environ.get('REMINDER_RECIPIENTS_EMAIL').split(',')

    this_week_service_date_str, following_service_date_str, _, _= service_dates()
    this_week_services_query = Service.objects.filter(service_date=str2date(this_week_service_date_str))

    # Send email reminder to servants who have services in this week.
    emails = ';'.join([servant.email for service in this_week_services_query.all() for servant in service.servants.all()])

    context = {'services': this_week_services_query,
               'this_week_date': this_week_service_date_str,
               'emails': emails}

    email_subject = render_to_string(
        'users/reminder_email_subject.txt', context).replace('\n', '')
    email_body = render_to_string('users/reminder_email_body.txt', context)


    send_mail(
        email_subject,
        email_body,
        sender_email,
        recipient_emails,
        fail_silently=False,
    )

    return "Reminder email sent."


@task(name='send_email_async')
def send_mail_async(kwargs):
    number_sent = send_mail(**kwargs)
    return number_sent