from django.shortcuts import render, redirect
from django.views.generic import View, ListView, DeleteView, DetailView, CreateView, UpdateView
from catalog.models import Group, Member, Service
from catalog.forms import MemberForm, ServiceForm, ResendActivationEmailForm
from django.urls import reverse_lazy
from django.http import HttpResponse
from django.utils.decorators import method_decorator
from django.contrib.messages import error, success
from django.template.response import TemplateResponse

from django.contrib.auth.tokens import default_token_generator as token_generator
from django.contrib.auth import (get_user, get_user_model, logout)
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.debug import sensitive_post_parameters

import datetime as dt
from .utils import (MailContextViewMixin)
from .forms import (UserCreationForm)


def index(request):
    """View function for home page of site."""

    # Generate counts of some of the main objects
    num_members = Member.objects.all().count()
    # num_groups = Service.

    # Available members (status = 'a')
    # num_instances_available = BookInstance.objects.filter(status__exact='a').count()

    # The 'all()' is implied by default.
    num_groups = Group.objects.count()

    # service
    today_full_date = dt.datetime.today()

    today_str = dt.datetime.strftime(today_full_date, '%Y-%m-%d')
    today_wk_int = int(dt.datetime.strftime(today_full_date, '%w'))

    delta_days_to_fri = 5 - today_wk_int

    if delta_days_to_fri == -2:
        # next week
        service_date = today_full_date + dt.timedelta(5)

    elif delta_days_to_fri == -1:
        # this week
        service_date = today_full_date - dt.timedelta(1)
    else:
        service_date = today_full_date + dt.timedelta(delta_days_to_fri)

    # the service date a week after
    following_service_date = service_date + dt.timedelta(7)

    service_date_str = service_date.strftime('%Y-%m-%d')
    following_service_date_str = following_service_date.strftime('%Y-%m-%d')

    services = Service.objects.filter(service_date=service_date_str)
    following_week_services = Service.objects.filter(service_date=following_service_date_str)

    context = {
        'num_members': num_members,
        'num_groups': num_groups,
        'services': services,
        'following_wk_services': following_week_services,
    }

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'catalog/index.html', context=context)


class MemberCreateView(CreateView):
    model = Member
    form_class = MemberForm
    template_name = 'catalog/member_form.html'


class MemberUpdateView(UpdateView):
    model = Member
    template_name = 'catalog/member_form.html'
    form_class = MemberForm


class MemberDeleteView(DeleteView):
    model = Member
    # template_name = 'user/member_delete.html'
    success_url = reverse_lazy('member_list')


class MemberListView(ListView):
    model = Member
    context_object_name = 'member_list'
    queryset = Member.objects.filter()
    template_name = 'catalog/member_list.html'


class MemberDetailView(DetailView):
    model = Member


class GroupListView(ListView):
    model = Group

    context_object_name = 'group_list'
    queryset = Group.objects.filter()
    template_name = 'catalog/group_list.html'


class GroupDetailView(DetailView):
    model = Group

# services


class ServiceCreateView(CreateView):
    model = Service
    form_class = ServiceForm


class ServiceUpdateView(UpdateView):
    model = Service
    form_class = ServiceForm


class ServiceDeleteView(DeleteView):
    model = Service


class ServiceListView(ListView):
    model = Service
    context_object_name = 'service_list'
    queryset = Service.objects.filter()
    template_name = 'catalog/service_list.html'


class ServiceDetailView(DetailView):
    model = Service

    context_object_name = 'service'
    template_name = 'catalog/service_detail.html'
    queryset = Service.objects.filter()

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