from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.views.generic import View, ListView, DeleteView, DetailView, CreateView, UpdateView
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.contrib.messages import error, success
from django.template.response import TemplateResponse
from django.contrib.auth.tokens import default_token_generator as token_generator
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import (get_user_model)
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.debug import sensitive_post_parameters
from tablib import Dataset
import datetime as dt1
from django_filters.views import FilterView
import django_tables2
from django_tables2.paginators import LazyPaginator

# Project imports
from catalog.decorators import class_login_required, require_authenticated_permission
from catalog.utils import MailContextViewMixin
from .models import User, Profile
from .utils import ProfileGetObjectMixin, UserGetObjectMixin, SERMON_GROUP
from .tables import UserTable, UserFilter
from .forms import UserForm, ProfileForm, RegistrationForm, ResendActivationEmailForm
from .resources import UserResource

# Create your views here.


@require_authenticated_permission('users.user_create')
class UserCreateView(CreateView):
    # model = Member
    template_name = 'users/user_form.html'
    form_class = UserForm
    success_message = 'Success: User was created.'
    success_url = reverse_lazy('user_list')


@class_login_required
class UserDetailView(DetailView):
    model = User


@class_login_required
class UserListView(django_tables2.SingleTableMixin, FilterView, LoginRequiredMixin):
    model = User
    table_class = UserTable
    filterset_class = UserFilter
    context_object_name = 'user_list'

    template_name = 'users/user_list.html'
    # paginator_class = LazyPaginator
    table_pagination = {"per_page": 10}

    def get_table_kwargs(self):
        return {"template_name": "django_tables2/bootstrap.html"}

    def get_context_data(self, *args, **kwargs):
        # Call the base implementation first to get a context
        context = super(UserListView, self).get_context_data(*args, **kwargs)
        # add whatever to your context:
        # context['whatever'] = "MORE STUFF"
        return context

    def get_queryset(self):
        current_user =self.request.user
        if current_user.is_superuser:
            queryset = User.objects.all()
        else:
            # Filter out sunday service members for non-superuser users
            queryset = User.objects.filter().exclude(group__name__in=SERMON_GROUP)
        return queryset


@require_authenticated_permission('users.user_update')
class UserUpdateView(UpdateView):
    model = User
    # template_name = 'users/user_update.html'
    form_class = UserForm
    success_message = 'Success: User was updated.'
    success_url = reverse_lazy('user_list')


@require_authenticated_permission('users.user_delete')
class UserDeleteView(DeleteView):
    model = User
    # template_name = 'users/user_confirm_delete.html'
    success_url = reverse_lazy('user_list')
    success_message = 'Success: User was deleted.'


@class_login_required
class ProfileDetailView(ProfileGetObjectMixin, DetailView):
    model = Profile
    template_name = 'users/profile_detail.html'


@class_login_required
class ProfileUpdateView(UserGetObjectMixin, UpdateView):
    model = User
    form_class = ProfileForm
    queryset = User.objects.filter()
    template_name = 'users/profile_update.html'

    success_message = 'Success: Profile was updated.'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile'] = reverse_lazy('group_create')
        return context

    def get_success_url(self):
        profile_slug = self.kwargs['slug']
        return reverse_lazy('profile_detail', args=[profile_slug])


# User account creation and activation
class ActivateAccount(View):
    success_url = reverse_lazy('login')
    template_name = 'users/user_activate_fail.html'

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
    form_class = RegistrationForm
    success_url = reverse_lazy('create_done')
    template_name = 'users/user_create.html'

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
            # email = bound_form.cleaned_data.get('email')
            # valid_user = User.objects.filter(email=email).count()
            # if not valid_user:
            #     error(request, 'Not a valid user.')
            #     return HttpResponse('<h1>Not a valid user.</h1>')

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


class ResendActivationEmail(MailContextViewMixin, View):
    form_class = ResendActivationEmailForm
    success_url = reverse_lazy('login')
    template_name = 'users/resend_activation.html'

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
                    bound_form.errors.pop('__all__')
                return TemplateResponse(
                    request,
                    self.template_name,
                    {'form': bound_form})
        success(request, 'Activation Email Sent!')
        return redirect(self.success_url)


# Export the users to excel
@login_required()
def user_export(request):
    person_resource = UserResource()
    dataset = person_resource.export()
    response = HttpResponse(dataset.xls, content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename="LLF contacts.xls"'
    return response


# Import users from excel
@login_required()
def user_import(request):
    if request.method == 'POST':
        resource = UserResource()
        dataset = Dataset()
        new_persons = request.FILES['external-file']

        imported_data = dataset.load(new_persons.read())

        imported_data.headers = ['Chinese Name', 'English Name', 'Gender', 'christian', 'Phone Number',\
                                 'Email', 'wechat_id', 'address', 'Job', 'Hometown', 'note',
                                 'first visit', 'birthday', 'lunar birthday', 'Habits']
        convert_first_visit = lambda drow: dt1.datetime(1899,12,30)+dt1.timedelta(days=int(drow[11])) if drow[11] else None
        convert_birthday = lambda drow: dt1.datetime(1899,12,30) + dt1.timedelta(days=int(drow[12])) if drow[12] else None
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

    return render(request, 'users/simple_upload.html')
