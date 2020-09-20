from celery import task
from django.template.loader import render_to_string
from django.core.mail import send_mail
import os
# project imports
from catalog.models import Service
from catalog.utils import service_dates, str2date


# Send reminders of the services of the upcoming week
@task(name='send_service_reminders')
def send_service_reminders():
    sender_email = os.environ.get('EMAIL_HOST_USER')
    # recipient_emails = os.environ.get('REMINDER_RECIPIENTS_EMAIL').split(',')

    this_week_service_date_str, _, _, _ = service_dates()
    this_week_services_query = Service.objects.filter(service_date=str2date(this_week_service_date_str))

    # Send email reminder to servants who have services in this week.
    unique_emails = set([servant.email for service in this_week_services_query.all() for servant in service.servants.all()])
    recipient_emails_str = ';'.join(list(unique_emails))
    recipient_emails = unique_emails
    # print(recipient_emails_str)

    # Build email content
    context = {'services': this_week_services_query,
               'this_week_date': this_week_service_date_str,
               'emails': recipient_emails_str}

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
    sender_email = os.environ.get('EMAIL_HOST_USER')
    _, following_service_date_str, _, _ = service_dates()
    bible_study_prep_service = Service.objects.filter(service_date=str2date(following_service_date_str),
                                                      categories__name__in=('查经设计', '查经设计协助')).all()
    # create recipient emails
    unique_emails = set([servant.email for service in bible_study_prep_service for servant in service.servants.all()])
    recipient_emails_str = ';'.join(list(unique_emails))
    recipient_emails = unique_emails
    # print(recipient_emails_str)

    # Build email content
    context = {'services': bible_study_prep_service,
               'the_following_week_date': following_service_date_str,
               'emails': recipient_emails_str}

    email_subject = render_to_string('users/reminder_bs_prep_email_subject.txt', context).replace('\n', '')
    email_body = render_to_string('users/reminder_bs_prep_email_body.txt', context)

    # Send email
    send_mail(
        email_subject,
        email_body,
        sender_email,
        recipient_emails,
        fail_silently=False,
    )

    return "Prep reminder email sent."


def send_mail_async(kwargs):
    number_sent = send_mail(**kwargs)
    return number_sent