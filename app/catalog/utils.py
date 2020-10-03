# app/catalog/utils.py
from logging import CRITICAL, ERROR
from smtplib import SMTPException
from django.conf import settings
from django.contrib.auth import get_user
from django.contrib.auth.tokens import default_token_generator as token_generator
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.mixins import  UserPassesTestMixin

from django.contrib.sites.shortcuts import get_current_site
from django.core.exceptions import ValidationError
from django.template.loader import render_to_string

from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.urls import reverse_lazy

from django.http import HttpResponse

from django.core.mail import EmailMessage, send_mail, BadHeaderError
from crispy_forms.layout import LayoutObject, TEMPLATE_PACK
from datetime import datetime as dt
import logging, traceback #, pandas as pd
import datetime

# Project imports
from users.models import User

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
        if 'request_submitter' in kwargs:
            context['request_submitter'] = kwargs.get('request_submitter')
        return render_to_string(
            email_template_name, context)

    def get_subject(self, **kwargs):
        subject_template_name = kwargs.get(
            'subject_template_name')
        context = kwargs.get('context')
        if 'request_submitter' in kwargs:
            context['request_submitter'] = kwargs.get('request_submitter')

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

        requester = User.objects.filter(email=request.POST['email']).first()
        token = token_generator.make_token(requester)
        uid = urlsafe_base64_encode(
            force_bytes(requester.pk))

        context.update({
            'domain': current_site.domain,
            'protocol': protocol,
            'site_name': current_site.name,
            'token': token,
            'uid': uid,
            # 'user': user,
            'requester': requester,
        })
        return context

    def _send_mail(self, request, recipient, **kwargs):
        kwargs['context'] = self.get_context_data(
            request, recipient)

        mail_kwargs = {
            "subject": self.get_subject(**kwargs),
            "message": self.get_message(**kwargs),
            "from_email": (
                settings.DEFAULT_FROM_EMAIL),
            "recipient_list": [recipient.email],
        }

        try:
            # from catalog.tasks import send_mail_async

            # number_sent = send_mail_async.delay(kwargs=mail_kwargs)
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

    def send_mail(self, recipient, **kwargs):
        """
        Send email to recipients
        :param recipient:
        :param kwargs:
        :return:
        """
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
        # kwargs['request_submitter'] = User.objects.filter(email=request.POST['email']).first()
        # print('')
        self._mail_sent, error = (
            self._send_mail(request, recipient, **kwargs)
        )

        if not self.mail_sent:
            self.add_error(
                None,  # no field - form error
                ValidationError(
                    self.mail_validation_error,
                    code=error))
        return self.mail_sent


class MailContextViewMixin:
    email_template_name = 'users/_email_create.txt'
    subject_template_name = (
        'users/_subject_create.txt')

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


# def handle_uploaded_schedules(raw_data, resource_instance):
#     # bank name
#     df = raw_data.df
#     df.dropna(subset=['Date'], inplace=True)
#     df.drop([41], inplace=True)
#     convert_date = lambda date: dt.datetime(1899, 12, 30) + dt.timedelta(days=int(date)) if isinstance(date, float) else date
#     df['Date'] = df['Date'].apply(convert_date)
#
#     categories, dates, servants, notes = list(), list(), list(), list()
#
#     for index, r in df.iterrows():
#         sevs = r.to_dict()
#         date = r[0]
#         BS_servants = list()
#         # iterate dict of a week's service team
#         for key, val in sevs.items():
#             # Escape the columns
#             if key in ('Date', 'Unnamed: 21'):
#                 continue
#             # Save the BS leaders
#             if 'BS-G' in key:
#                 BS_servants.append(val)
#                 continue
#             else:
#                 dates.append(date)
#                 categories.append(key)
#
#                 if key.lower() in ['content', 'sharing', 'reminder', 'prayer-meeting', 'clean-up', 'dish-wash']:
#                     notes.append(val)
#                     servants.append(None)
#                 else:
#                     notes.append(None)
#                     servants.append(val)
#         # Save BS leaders
#         if type(BS_servants[0]) == str:
#             dates.append(date)
#             categories.append('Bible-study-servants')
#             servants.append(','.join(BS_servants))
#             notes.append(None)
#
#     data = {'Date': dates, 'Category': categories,
#             'Servants': servants, 'Note': notes}
#     ndf = pd.DataFrame(data)
#     ndf['id'] = range(1, len(ndf['Date']) + 1)
#     ndf['id'].astype('int64')
#
#     # Iterate through rows
#     for index, row in ndf.iterrows():
#
#         d = row.to_dict()
#         servants = d.get('Servants')
#
#         print(f"Service: {d.get('Date')}, {d.get('Category')}")
#         if not d.get('Category'):
#             continue
#
#         # Create a service instance
#         service = Service(
#             # id=d.get('id'),
#                           service_category=d.get('Category'),
#                           service_date=d.get('Date'),
#                           service_note=d.get('Note'))
#         service.save()
#         if isinstance(servants, str):
#             # print('Servants: ' + servants)
#             servants = servants.strip()
#             servants = servants.replace('/', ',').replace('、', ',')
#             if ',' in servants:
#
#                 sns = servants.split(',')
#             elif ' ' in servants:
#                 sns = servants.split(' ')
#             else:
#                 sns = [servants]
#
#             for servant_name in sns:
#                 try:
#                     servant = User.objects.get(name=servant_name)
#                     service.servants.add(servant)
#                 except:
#                     print("Cannot find servant: {}".format(servant_name))
#
#     # # output the new dataframe to csv
#     # ndf.to_csv('temp/temp.csv', index=False)
#     #
#     # imported_data = Dataset().load(open('temp/temp.csv', encoding='utf-8').read())
#     # result = resource_instance.import_data(imported_data, dry_run=True)  # Test the data import
#     # # errors = result.has_errors()
#     #
#     # if not result.has_errors():
#     #     resource_instance.import_data(imported_data, dry_run=False)  # Actually import now


def service_dates():
    """
    Get the service dates in string of this week and the next week.
    :return: tuple. (this_week_service_date_str in YYYY-MM-DD format,
                     following_week_service_date_str in YYYY-MM-DD format,
                     this_week_sunday_date_str in YYYY-MM-DD format,
                     following_week_sunday_date_str in YYYY-MM-DD)
    """
    today_full_date = dt.today()

    today_wk_int = int(dt.strftime(today_full_date, '%w'))

    delta_days_to_fri = 5 - today_wk_int

    if delta_days_to_fri == -2:
        # The date of next week
        service_date = today_full_date + datetime.timedelta(5)

    elif delta_days_to_fri == -1:
        # The date of this week
        service_date = today_full_date - datetime.timedelta(1)
    else:
        service_date = today_full_date + datetime.timedelta(delta_days_to_fri)

    # The service date a week after
    following_service_date = service_date + datetime.timedelta(7)

    # This week's Sunday date
    this_week_sunday_date = service_date + datetime.timedelta(2)
    # Next weeks' Sunday date
    following_week_sunday_date = following_service_date + datetime.timedelta(2)

    this_week_service_date_str = service_date.strftime('%Y-%m-%d')
    following_week_service_date_str = following_service_date.strftime('%Y-%m-%d')
    this_week_sunday_date_str = this_week_sunday_date.strftime('%Y-%m-%d')
    following_week_sunday_date_str = following_week_sunday_date.strftime('%Y-%m-%d')

    return this_week_service_date_str, following_week_service_date_str, this_week_sunday_date_str, following_week_sunday_date_str


def date2str(date):
    return datetime.datetime.strftime(date, '%Y-%m-%d')


def str2date(date_str):
    try:
        if '/' in date_str:
            return datetime.datetime.strptime(date_str, '%m/%d/%Y').date()
        else:
            return datetime.datetime.strptime(date_str, '%Y-%m-%d').date()
    except:
        return None


#Formset for bulk create use
class Formset(LayoutObject):
    template = "catalog/formset.html"

    def __init__(self, formset_name_in_context, template=None):
        self.formset_name_in_context = formset_name_in_context
        self.fields = []
        if template:
            self.template = template

    def render(self, form, form_style, context, template_pack=TEMPLATE_PACK):
        formset = context[self.formset_name_in_context]
        return render_to_string(self.template, {'formset': formset})


# permission decorators and Mixins
is_staff_or_supervisor = user_passes_test(lambda u: u.is_staff or u.is_superuser, login_url=reverse_lazy('catalog_index'))
is_supervisor = user_passes_test(lambda u: u.is_superuser, login_url=reverse_lazy('catalog_index'))


def staff_or_supervisor_required(view_func):
    decorated_view_func = login_required(is_staff_or_supervisor(view_func))
    return decorated_view_func


def supervisor_required(view_func):
    decorated_view_func = login_required(is_supervisor(view_func))
    return decorated_view_func


class UserPassesTestMixinCustom(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_staff or self.request.user.is_superuser


# Export helper function
def export_data(file_format, dataset, filename):
    """
    Export data to external files in a given format.
    :param file_format:
    :param dataset:
    :param filename:
    :return:
    """
    response = None
    if file_format == 'CSV':
        response = HttpResponse(dataset.csv, content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename="{filename}.csv"'

    elif file_format == 'JSON':
        response = HttpResponse(dataset.json, content_type='application/json')
        response['Content-Disposition'] = f'attachment; filename="{filename}.json"'

    elif file_format == 'Excel':
        response = HttpResponse(dataset.xls, content_type='application/vnd.ms-excel')
        response['Content-Disposition'] = f'attachment; filename="{filename}.xls"'

    return response