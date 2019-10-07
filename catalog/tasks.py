from celery import task
from django.template.loader import render_to_string
from django.core.mail import send_mail
from .models import Service, service_dates
import os


@task(name='send_reminders')
def send_reminders():
    sender_email = os.environ.get('EMAIL_HOST_USER')
    recipient_emails = os.environ.get('REMINDER_RECIPIENTS_EMAIL').split(',')

    this_week_service_date_str, following_service_date_str, _ = service_dates()
    this_week_services = Service.objects.filter(service_date=this_week_service_date_str)

    context = {'services': this_week_services,
               'this_week_date': this_week_service_date_str}

    email_subject = render_to_string(
        'catalog/reminder_email_subject.txt', context).replace('\n', '')
    email_body = render_to_string('catalog/reminder_email_body.txt', context)

    send_mail(
        email_subject,
        email_body,
        sender_email,
        recipient_emails,
        fail_silently=False,
    )

    return "Reminder email sent."
