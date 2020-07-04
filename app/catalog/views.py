from django.shortcuts import render, redirect
from django.views.generic import View, ListView, DeleteView, DetailView, CreateView, UpdateView
from app.catalog.models import Group, Member, Service, ServiceTable, ServiceFilter
from app.catalog import MemberForm, ServiceForm, GroupForm, ServiceUpdateForm, ResendActivationEmailForm, UserCreationForm
from app.catalog import MemberResource, ServiceResource
from django.urls import reverse_lazy
from django.http import HttpResponse
from django.utils.decorators import method_decorator
from django.contrib.messages import error, success
from django.template.response import TemplateResponse

from django.contrib.auth.tokens import default_token_generator as token_generator
from django.contrib.auth import (get_user_model)
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.debug import sensitive_post_parameters
from django_filters.views import FilterView
from bootstrap_modal_forms.generic import (BSModalCreateView,
                                           BSModalUpdateView,
                                           BSModalDeleteView)
import django_tables2
from django.contrib.auth.decorators import login_required
from .decorators import class_login_required, require_authenticated_permission

# import datetime as dt
from .utils import (MailContextViewMixin, handle_uploaded_schedules)
from .models import service_dates
from .tasks import send_reminders
from tablib import Dataset
import datetime as dt


def test_email(request):
    send_reminders.delay()
    return HttpResponse("Email sent.")


# @login_required()
class IndexView(ListView):
    model = Service
    # table_class = ServiceTable
    queryset = Service.objects.filter(service_date=service_dates()[0])
    context_object_name = 'services'
    template_name = "catalog/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        this_week_service_date_str, following_service_date_str, _ = service_dates()
        # services = Service.objects.filter(service_date=this_week_service_date_str)
        following_week_services = Service.objects.filter(service_date=following_service_date_str)

        context['next_services'] = following_week_services

        context['this_week_service_date'] = this_week_service_date_str
        context['next_week_service_date'] = following_service_date_str
        return context


@require_authenticated_permission('catalog.member_create')
class MemberCreateView(BSModalCreateView):
    # model = Member
    template_name = 'catalog/member_form.html'
    form_class = MemberForm
    success_message = 'Success: Member was created.'
    success_url = reverse_lazy('member_list')


@require_authenticated_permission('catalog.member_update')
class MemberUpdateView(BSModalUpdateView):
    model = Member
    template_name = 'catalog/member_update.html'
    form_class = MemberForm
    success_message = 'Success: Member was updated.'
    success_url = reverse_lazy('member_list')


@require_authenticated_permission('catalog.member_delete')
class MemberDeleteView(BSModalDeleteView):
    model = Member
    template_name = 'catalog/member_confirm_delete.html'
    success_url = reverse_lazy('member_list')
    success_message = 'Success: Member was deleted.'


@class_login_required
class MemberListView(ListView):
    model = Member
    context_object_name = 'member_list'
    queryset = Member.objects.filter()
    template_name = 'catalog/member_list.html'


@class_login_required
class MemberDetailView(DetailView):
    model = Member

# Export the members to excel
@login_required()
def member_export(request):
    person_resource = MemberResource()
    dataset = person_resource.export()
    response = HttpResponse(dataset.xls, content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename="LLF contacts.xls"'
    return response

# Import members from excel
@login_required()
def member_import(request):
    if request.method == 'POST':
        resource = MemberResource()
        dataset = Dataset()
        new_persons = request.FILES['external-file']

        imported_data = dataset.load(new_persons.read())

        imported_data.headers = ['Chinese Name', 'English Name', 'Gender', 'christian', 'Phone Number',\
                                 'Email', 'wechat_id', 'address', 'Job', 'Hometown', 'note',
                                 'first visit', 'birthday', 'lunar birthday', 'Habits']
        convert_first_visit = lambda drow: dt.datetime(1899,12,30)+dt.timedelta(days=int(drow[11])) if drow[11] else None
        convert_birthday = lambda drow: dt.datetime(1899,12,30) + dt.timedelta(days=int(drow[12])) if drow[12] else None
        convert_christian_column = lambda drow: True if drow[3]=='是' else False
        imported_data.append_col(convert_first_visit, header='First Visit Time')
        imported_data.append_col(convert_birthday, header='Birthday')
        imported_data.append_col(convert_christian_column, header='Christian')

        # add columns
        imported_data.append_col(range(len(imported_data['Chinese Name'])), header='id')
        imported_data.append_col([True]*len(imported_data['Chinese Name']), header='active')
        imported_data.append_col([False]*len(imported_data['Chinese Name']), header='group_leader')
        # imported_data.append_col([1]*len(imported_data['Chinese Name']), header='group_id')
        imported_data.append_col([None] * len(imported_data['Chinese Name']), header='username')
        imported_data.append_col([None] * len(imported_data['Chinese Name']), header='slug')

        # remove some columns
        del imported_data['first visit']
        del imported_data['christian']
        del imported_data['birthday']
        del imported_data['wechat_id']
        del imported_data['address']
        del imported_data['note']
        del imported_data['lunar birthday']

        # Test the data import
        result = resource.import_data(imported_data, dry_run=True)

        # Actually import now
        if not result.has_errors():
            results = resource.import_data(imported_data, dry_run=False)
            errors = results.has_errors()

    return render(request, 'catalog/simple_upload.html')


@class_login_required
class GroupListView(ListView):
    model = Group

    context_object_name = 'group_list'
    queryset = Group.objects.filter()
    template_name = 'catalog/group_list.html'


@class_login_required
class GroupDetailView(DetailView):
    model = Group


@class_login_required
class GroupCreateView(BSModalCreateView):
    template_name = 'catalog/group_form.html'
    form_class = GroupForm
    success_message = 'Success: Group was created.'
    success_url = reverse_lazy('group_list')

# services


@require_authenticated_permission('catalog.service_create')
class ServiceCreateView(CreateView):
    model = Service
    form_class = ServiceForm
    template_name = 'catalog/service_form.html'

    def get_form(self):
        form = super(ServiceCreateView, self).get_form()
        form.fields['service_date'].widget.attrs.update({'class': 'datepicker'})
        return form


@require_authenticated_permission('catalog.service_update')
class ServiceUpdateView(UpdateView):
    model = Service
    form_class = ServiceUpdateForm

    def get_context_data(self, **kwargs):
        context = super(ServiceUpdateView, self).get_context_data(**kwargs)
        category = context.get('service').service_category
        context['category'] = category
        return context


@require_authenticated_permission('catalog.service_delete')
class ServiceDeleteView(DeleteView):
    model = Service
    success_url = reverse_lazy('service_list')


# @class_login_required
# class ServiceListView(ListView):
#     model = Service
#     context_object_name = 'service_list'
#     queryset = Service.objects.filter()
#     template_name = 'catalog/service_list.html'


@class_login_required
class ServiceDetailView(DetailView):
    model = Service

    context_object_name = 'service'
    template_name = 'catalog/service_detail.html'
    queryset = Service.objects.filter()


@class_login_required
class ServiceListView(django_tables2.SingleTableMixin, FilterView):
    model = Service
    table_class = ServiceTable
    queryset = Service.objects.all()
    filterset_class = ServiceFilter
    template_name = "catalog/service_list.html"

    table_pagination = {"per_page": 10}

    def get_table_kwargs(self):
        return {"template_name": "django_tables2/bootstrap.html"}


@login_required()
def load_services(request):

    services = set([s.service_category for s in Service.objects.all()])
    return render(request,
                  'catalog/service_category_list_options.html',
                  {'services': services})


# Export the services to excel
@login_required()
def service_export(request):
    resource = ServiceResource()
    dataset = resource.export()
    response = HttpResponse(dataset.xls, content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename="LLF service schedule.xls"'
    return response


# Import services from excel
@login_required()
def service_import(request):

    if request.method == 'POST':
        resource = ServiceResource()
        dataset = Dataset()
        loaded_file = request.FILES['external-file']

        imported_data = dataset.load(loaded_file.read())
        handle_uploaded_schedules(imported_data, resource)
        # imported_data.headers = ['service_date', 'leader_of_week', 'setup_group', 'food_pickup', 'fruit_dessert',\
        #                          'dish_clean', 'child_care', 'newcomer_welcome', 'birthday_celebrate', 'worship', 'bible_study',
        #                          'first visit', 'birthday', 'lunar birthday', 'Habits']

        # convert_first_visit = lambda drow: dt.datetime(1899,12,30)+dt.timedelta(days=int(drow[11])) if drow[11] else None

    return render(request, 'catalog/simple_upload.html')


# User account creation and activation
class ActivateAccount(View):
    success_url = reverse_lazy('login')
    template_name = 'catalog/user_activate.html'

    @method_decorator(never_cache)
    def get(self, request, uidb64, token):
        User = get_user_model()
        try:
            # urlsafe_base64_decode()
            #     -> bytestring in Py3
            uid = force_text(
                urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError,
                OverflowError, User.DoesNotExist):
            user = None
        if (user is not None
                and token_generator
                .check_token(user, token)):
            user.is_active = True
            user.save()
            success(
                request,
                'User Activated! '
                'You may now login.')
            return redirect(self.success_url)
        else:
            return TemplateResponse(
                request,
                self.template_name)


class CreateAccount(MailContextViewMixin, View):
    form_class = UserCreationForm
    success_url = reverse_lazy(
        'create_done')
    template_name = 'catalog/user_create.html'

    @method_decorator(csrf_protect)
    def get(self, request):
        return TemplateResponse(
            request,
            self.template_name,
            {'form': self.form_class()})

    @method_decorator(csrf_protect)
    @method_decorator(sensitive_post_parameters(
        'password1', 'password2'))
    def post(self, request):
        bound_form = self.form_class(request.POST)
        if bound_form.is_valid():
            email = bound_form.cleaned_data.get('email')
            valid_member = Member.objects.filter(email=email).count()
            if not valid_member:
                error(request, 'Not a valid member.')
                return HttpResponse('<h1>Not a valid member.</h1>')
            # not catching returned user
            bound_form.save(
                **self.get_save_kwargs(request))
            if bound_form.mail_sent:  # mail sent?
                return redirect(self.success_url)
            else:
                errs = (
                    bound_form.non_field_errors())
                for err in errs:
                    error(request, err)
                return redirect(
                    'resend_activation')

        return TemplateResponse(
            request,
            self.template_name,
            {'form': bound_form})


class ResendActivationEmail(
        MailContextViewMixin, View):
    form_class = ResendActivationEmailForm
    success_url = reverse_lazy('login')
    template_name = 'catalog/resend_activation.html'

    @method_decorator(csrf_protect)
    def get(self, request):
        return TemplateResponse(
            request,
            self.template_name,
            {'form': self.form_class()})

    @method_decorator(csrf_protect)
    def post(self, request):
        bound_form = self.form_class(request.POST)
        if bound_form.is_valid():
            user = bound_form.save(
                **self.get_save_kwargs(request))
            if (user is not None
                    and not bound_form.mail_sent):
                errs = (
                    bound_form.non_field_errors())
                for err in errs:
                    error(request, err)
                if errs:
                    bound_form.errors.pop(
                        '__all__')
                return TemplateResponse(
                    request,
                    self.template_name,
                    {'form': bound_form})
        success(
            request,
            'Activation Email Sent!')
        return redirect(self.success_url)