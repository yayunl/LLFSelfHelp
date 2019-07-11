from celery import task
from django.core.mail import send_mail
import os


@task(name='send_reminders')
def send_reminders():

    from_email = os.environ.get('EMAIL_HOST_USER')
    send_mail(
        'Subject here',
        'Here is the message.',
        from_email,
        [from_email],
        fail_silently=False,
    )

    return "Email sent."
