import logging
import traceback
from logging import CRITICAL, ERROR
from smtplib import SMTPException
import datetime as dt
from django.conf import settings
from django.contrib.auth import get_user
from django.contrib.auth.tokens import \
    default_token_generator as token_generator
from django.contrib.sites.shortcuts import \
    get_current_site
from django.core.exceptions import ValidationError
from django.core.mail import (
    BadHeaderError, send_mail)
from django.template.loader import \
    render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import \
    urlsafe_base64_encode
from django.template import Context, Template
from django.core.mail import EmailMessage
from .models import Service

logger = logging.getLogger(__name__)


class ActivationMailFormMixin:
    mail_validation_error = ''

    def log_mail_error(self, **kwargs):
        msg_list = [
            'Activation email did not send.\n',
            'from_email: {from_email}\n'
            'subject: {subject}\n'
            'message: {message}\n',
        ]
        recipient_list = kwargs.get(
            'recipient_list', [])
        for recipient in recipient_list:
            msg_list.insert(
                1, 'recipient: {r}\n'.format(
                    r=recipient))
        if 'error' in kwargs:
            level = ERROR
            error_msg = (
                'error: {0.__class__.__name__}\n'
                'args: {0.args}\n')
            error_info = error_msg.format(
                kwargs['error'])
            msg_list.insert(1, error_info)
        else:
            level = CRITICAL
        msg = ''.join(msg_list).format(**kwargs)
        logger.log(level, msg)

    @property
    def mail_sent(self):
        if hasattr(self, '_mail_sent'):
            return self._mail_sent
        return False

    @mail_sent.setter
    def set_mail_sent(self, value):
        raise TypeError(
            'Cannot set mail_sent attribute.')

    def get_message(self, **kwargs):
        email_template_name = kwargs.get(
            'email_template_name')
        context = kwargs.get('context')
        return render_to_string(
            email_template_name, context)

    def get_subject(self, **kwargs):
        subject_template_name = kwargs.get(
            'subject_template_name')
        context = kwargs.get('context')
        subject = render_to_string(
            subject_template_name, context)
        # subject *must not* contain newlines
        subject = ''.join(subject.splitlines())
        return subject

    def get_context_data(
            self, request, user, context=None):
        if context is None:
            context = dict()
        current_site = get_current_site(request)
        if request.is_secure():
            protocol = 'https'
        else:
            protocol = 'http'
        token = token_generator.make_token(user)
        uid = urlsafe_base64_encode(
            force_bytes(user.pk))
        context.update({
            'domain': current_site.domain,
            'protocol': protocol,
            'site_name': current_site.name,
            'token': token,
            'uid': uid,
            'user': user,
        })
        return context

    def _send_mail(self, request, user, **kwargs):
        kwargs['context'] = self.get_context_data(
            request, user)
        mail_kwargs = {
            "subject": self.get_subject(**kwargs),
            "message": self.get_message(**kwargs),
            "from_email": (
                settings.DEFAULT_FROM_EMAIL),
            "recipient_list": [user.email],
        }
        try:
            # number_sent will be 0 or 1
            number_sent = send_mail(**mail_kwargs)
        except Exception as error:
            self.log_mail_error(
                error=error, **mail_kwargs)
            if isinstance(error, BadHeaderError):
                err_code = 'badheader'
            elif isinstance(error, SMTPException):
                err_code = 'smtperror'
            else:
                err_code = 'unexpectederror'
            return (False, err_code)
        else:
            if number_sent > 0:
                return (True, None)
        self.log_mail_error(**mail_kwargs)
        return (False, 'unknownerror')

    def send_mail(self, user, **kwargs):
        request = kwargs.pop('request', None)
        if request is None:
            tb = traceback.format_stack()
            tb = ['  ' + line for line in tb]
            logger.warning(
                'send_mail called without '
                'request.\nTraceback:\n{}'.format(
                    ''.join(tb)))
            self._mail_sent = False
            return self.mail_sent
        self._mail_sent, error = (
            self._send_mail(
                request, user, **kwargs))
        if not self.mail_sent:
            self.add_error(
                None,  # no field - form error
                ValidationError(
                    self.mail_validation_error,
                    code=error))
        return self.mail_sent


class MailContextViewMixin:
    email_template_name = 'catalog/email_create.txt'
    subject_template_name = (
        'catalog/subject_create.txt')

    def get_save_kwargs(self, request):
        return {
            'email_template_name':
                self.email_template_name,
            'request': request,
            'subject_template_name':
                self.subject_template_name,
        }


class ProfileGetObjectMixin:

    def get_object(self, queryset=None):
        current_user = get_user(self.request)
        return current_user.profile


def service_dates():
    """
    Get the service dates in string of this week and the next week.
    :return: tuple. (this_week_service_date_str, following_week_service_date_str)
    """
    today_full_date = dt.datetime.today()

    today_wk_int = int(dt.datetime.strftime(today_full_date, '%w'))

    delta_days_to_fri = 5 - today_wk_int

    if delta_days_to_fri == -2:
        # The date of next week
        service_date = today_full_date + dt.timedelta(5)

    elif delta_days_to_fri == -1:
        # The date of this week
        service_date = today_full_date - dt.timedelta(1)
    else:
        service_date = today_full_date + dt.timedelta(delta_days_to_fri)

    # The service date a week after
    following_service_date = service_date + dt.timedelta(7)

    this_week_service_date_str = service_date.strftime('%Y-%m-%d')
    following_week_service_date_str = following_service_date.strftime('%Y-%m-%d')

    return this_week_service_date_str, following_week_service_date_str


def send_reminder_email(email):
    this_week_service_date_str, following_service_date_str = service_dates()
    this_week_services = Service.objects.filter(service_date=this_week_service_date_str)

    context = Context({'service': this_week_services})

    email_subject = render_to_string(
        'catalog/templates/catalog/reminder_email_subject.txt', context).replace('\n', '')
    email_body = render_to_string('catalog/templates/catalog/reminder_email_body.txt', context)

    email = EmailMessage(
        email_subject, email_body, email,
        [settings.DEFAULT_FROM_EMAIL], [],
        headers={'Reply-To': email}
    )
    print(email_subject)
    return email.send(fail_silently=False)