from celery import task
from .utils import send_reminder_email

#
# @task()
# def sum_two_numbers(a, b):
#     c = a+b
#     return c


@task()
def send_reminders():

    # following_week_services = Service.objects.filter(service_date=following_service_date_str)
    return send_reminder_email("YOUR_EMAIL@gmail.com")

