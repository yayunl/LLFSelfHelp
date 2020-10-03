from django.shortcuts import render, get_object_or_404
from django.views.generic import View, ListView, DeleteView, DetailView, CreateView, UpdateView
from django.urls import reverse_lazy
from django.http import HttpResponse, HttpResponseRedirect
from django.db.models import Q
from django.db import transaction
from django_filters.views import FilterView

from django.contrib.auth.decorators import login_required
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages

from .decorators import class_login_required, require_authenticated_permission
from datetime import datetime as dt
from itertools import chain
import django_tables2
from tablib import Dataset

# sub-level imports
from .models import Group, Service, Category, ServicesOfWeek
from .tables import ServiceTable, ServiceFilter
from .forms import ServiceForm, GroupForm, CategoryForm, ServicesOfWeekForm, ServiceFormSet
from .resources import ServiceResource, GroupResource, CategoryResource, SundaySermonResource
from .utils import (service_dates, str2date, date2str,
                    UserPassesTestMixinCustom,
                    is_staff_or_supervisor, is_supervisor,
                    export_data)
from .tasks import send_prep_reminder, send_service_reminder, send_birthday_reminder, send_coordinator_of_week_reminder

from users.models import User
from users.utils import SERMON_GROUP, SERMON_CATEGORY


@login_required()
@is_supervisor
def test_prep_email(request):
    send_prep_reminder.delay()
    return HttpResponse("Prep Email sent.")


@login_required()
@is_supervisor
def test_service_email(request):
    send_service_reminder.delay()
    return HttpResponse("Service Email sent.")


@login_required()
@is_supervisor
def test_birthday_email(request):
    send_birthday_reminder.delay()
    return HttpResponse("Birthday email sent.")


# admin page
@login_required()
@is_supervisor
def admin_page(request):
    return render(request, 'catalog/admin_page.html')


@login_required()
@is_supervisor
def test_coordinator_report_email(request):
    send_coordinator_of_week_reminder.delay()
    return HttpResponse("Coordinator report reminder email sent.")


# Home route
@class_login_required
class IndexView(ListView):
    model = Service
    # table_class = ServiceTable

    # Query services of this week
    queryset = Service.objects.filter(Q(service_date=str2date(service_dates()[0])) |
                                      Q(service_date=str2date(service_dates()[2])) )

    context_object_name = 'this_week_services'
    template_name = "catalog/index.html"
    success_message = 'Welcome!'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        this_week_service_date_str, following_service_date_str, _, _ = service_dates()
        # Query next week's services
        context['next_week_services'] = Service.objects.filter(Q(service_date=str2date(service_dates()[1])) |
                                                               Q(service_date=str2date(service_dates()[3])))

        context['this_week_service_date'] = this_week_service_date_str
        context['next_week_service_date'] = following_service_date_str
        # dt.month()
        context['member_birthday_of_month'] = User.objects.filter(birthday__month=dt.now().strftime('%m'))\
            .order_by('birthday__day').all()
        return context


# Groups
@class_login_required
class GroupCreateView(UserPassesTestMixinCustom, SuccessMessageMixin, CreateView):
    model = Group
    template_name = 'catalog/group_form.html'
    form_class = GroupForm
    # success_message = 'Group %(name)s was created.'
    # success_url = reverse_lazy('group_list')

    def form_valid(self, form):
        record = form.cleaned_data
        group_name, group_desc= record.get('name'), record.get('description')
        if Group.objects.filter(name=group_name, description=group_desc):
            messages.warning(self.request, 'Group: %s already existed!'%group_name)
        else:
            form.save()
            messages.success(self.request, 'Group: %s was created.'%group_name)
        return HttpResponseRedirect(reverse_lazy('group_list'))

    # def test_func(self):
    #     if self.request.user.is_staff:
    #         return True
    #     else:
    #         # messages.warning(self.request, "You are not allowed to edit.")
    #         return False


@class_login_required
class GroupListView(ListView):
    model = Group

    context_object_name = 'group_list'

    template_name = 'catalog/group_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['create_url'] = reverse_lazy('group_create')
        context['export_url'] = reverse_lazy('group_export')
        return context

    def get_queryset(self):
        current_user =self.request.user
        if current_user.is_superuser:
            queryset = Group.objects.all()
        else:
            # Filter out sunday service members for non-superuser users
            queryset = Group.objects.filter().exclude(name__in=SERMON_GROUP)
        return queryset


@class_login_required
class GroupUpdateView(UserPassesTestMixinCustom, SuccessMessageMixin, UpdateView):
    model = Group
    form_class = GroupForm
    success_url = reverse_lazy('group_list')
    success_message = 'Group: %(name)s was updated.'


@class_login_required
class GroupDetailView(DetailView):
    model = Group


@class_login_required
class GroupDeleteView(UserPassesTestMixinCustom, SuccessMessageMixin, DeleteView):
    model = Group
    success_url = reverse_lazy('group_list')
    success_message = 'Group %(name)s was deleted.'


# Categories
@class_login_required
class CategoryCreateView(UserPassesTestMixinCustom, SuccessMessageMixin, CreateView):

    model = Category
    template_name = 'catalog/group_form.html'
    form_class = CategoryForm

    def form_valid(self, form):
        record = form.cleaned_data
        try:
            cat = record.get('categories').first()
            ser_date = record.get('service_date')
            if not Service.objects.filter(service_date=ser_date, categories__name=cat.name):
                messages.warning(self.request, 'Category: %s exists in the database!' % cat.name)
            else:
                form.save()
                messages.success(self.request, 'Category: %s was created.' % cat.name)
        except:
            form.save()
            messages.success(self.request, 'Category: %s was created.' % record.get('name'))
        return HttpResponseRedirect(reverse_lazy('category_list'))


@class_login_required
class CategoryListView(ListView):
    model = Category
    context_object_name = 'category_list'

    template_name = 'catalog/category_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['create_url'] = reverse_lazy('category_create')
        context['export_url'] = reverse_lazy('category_export')
        return context

    def get_queryset(self):
        current_user =self.request.user
        if current_user.is_superuser:
            queryset = Category.objects.all()
        else:
            # Filter out sunday service members for non-superuser users
            queryset = Category.objects.filter().exclude(name__in=SERMON_CATEGORY)
        return queryset


@class_login_required
class CategoryUpdateView(UserPassesTestMixinCustom, SuccessMessageMixin, UpdateView):
    model = Category
    form_class = CategoryForm
    success_url = reverse_lazy('category_list')
    success_message = 'Category: %(name)s was updated.'


@class_login_required
class CategoryDetailView(DetailView):
    model = Category

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        object = context.get('object')
        # services as part of the category
        services = Service.objects.filter(categories__name=object.name).all()
        # servants as part of the services
        servants = set([ser for service in services for ser in service.servants.all() ])
        context['users_involved'] = servants
        return context


@class_login_required
class CategoryDeleteView(UserPassesTestMixinCustom, SuccessMessageMixin, DeleteView):
    model = Category
    success_url = reverse_lazy('category_list')
    success_message = 'Category %(name)s was deleted.'


# Bulk services
@class_login_required
class ServiceBulkCreateView(UserPassesTestMixinCustom, SuccessMessageMixin, CreateView):
    model = ServicesOfWeek
    form_class = ServicesOfWeekForm
    template_name = 'catalog/service_bulk_create.html'
    success_url = reverse_lazy('service_list')
    success_message = 'Services on %(services_date)s were created.'

    def get_context_data(self, **kwargs):
        data = super(ServiceBulkCreateView, self).get_context_data(**kwargs)
        if self.request.POST:
            data['services'] = ServiceFormSet(self.request.POST)
        else:
            data['services'] = ServiceFormSet()
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        services = context['services']
        record = form.cleaned_data
        service_date = record.get('services_date')
        service_forms = list()
        unique_cats = list()
        initial_forms_cnt = len(services.forms)
        with transaction.atomic():
            self.object = form.save()
            if services.is_valid():
                for service_form in services.forms:
                    cat_name = service_form.cleaned_data.get('categories').first().name
                    count = Service.objects.filter(service_date=service_date,
                                                   categories__name__in=[cat_name]).count()
                    # Ensure the service in the bulk does not exist in db.
                    if count == 0 and cat_name not in unique_cats:
                        service_forms.append(service_form)
                        service_form.instance.service_date = service_date
                    # Ensure the same service bulk does not have duplicates.
                    unique_cats.append(cat_name)
                services.forms = service_forms
                services.instance = self.object
                services.save()
        if len(service_forms) != initial_forms_cnt:
            messages.warning(self.request, 'Found some services already existed in the database. '
                                           'Duplicates are not saved.')
        else:
            messages.success(self.request, 'Services on %s were created.' % service_date)
        return super(ServiceBulkCreateView, self).form_valid(form)


# Services
@class_login_required
class ServiceCreateView(UserPassesTestMixinCustom, SuccessMessageMixin, CreateView):
    model = Service
    form_class = ServiceForm
    template_name = 'catalog/service_form.html'

    def get_form(self):
        form = super(ServiceCreateView, self).get_form()
        form.fields['service_date'].widget.attrs.update({'class': 'datepicker'})
        # Exclude Sunday service category from the LLF services.
        form.fields['categories'].queryset = Category.objects.filter().exclude(name__in=SERMON_CATEGORY)
        # Exclude Sunday service servants from the LLF servants.
        form.fields['servants'].queryset = User.objects.filter().exclude(group__name__in=SERMON_GROUP)
        return form

    def form_valid(self, form):
        record = form.cleaned_data
        service_date, service_cat_name = record.get('service_date'), record.get('categories').first().name

        count = Service.objects.filter(service_date=service_date, categories__name__in=[service_cat_name]).count()
        if count > 0:
            messages.warning(self.request, 'Service: %s on %s already existed!' % (service_cat_name, service_date))
        else:
            # form.fields['services_of_week']
            form.save()
            messages.success(self.request, 'Service: %s on %s was created.' % (service_cat_name, service_date))
        return HttpResponseRedirect(reverse_lazy('service_list'))


@class_login_required
class ServiceDetailView(DetailView):
    model = Service

    context_object_name = 'service'
    template_name = 'catalog/service_detail.html'
    queryset = Service.objects.filter()

    # def get_queryset(self):
    #     Service.objects.filter(name=self.kwargs['name'], service_)


@class_login_required
class ServiceListView(django_tables2.SingleTableMixin, FilterView):
    model = Service
    table_class = ServiceTable
    filterset_class = ServiceFilter

    queryset = Service.objects.all()

    template_name = "catalog/service_list.html"

    table_pagination = {"per_page": 10}

    # def get_table_kwargs(self):
    #     return {"template_name": "django_tables2/bootstrap.html"}

    # def get_queryset(self):
    #     service_date = str2date(service_dates()[0])
    #     queryset = Service.objects.filter(service_date__lt=service_date, service_date__gt=service_date).all()
    #     return queryset


@class_login_required
class ServiceUpdateView(UserPassesTestMixinCustom, SuccessMessageMixin, UpdateView):
    model = Service
    form_class = ServiceForm
    success_url = reverse_lazy('service_list')
    success_message = 'The service was updated.'


@class_login_required
class ServiceDeleteView(UserPassesTestMixinCustom, DeleteView):
    model = Service
    success_url = reverse_lazy('service_list')


# Sunday sermons
@class_login_required
class SundayServiceCreateView(UserPassesTestMixinCustom, SuccessMessageMixin, CreateView):
    model = Service
    form_class = ServiceForm
    template_name = 'catalog/service_form.html'
    queryset = Service.objects.filter()

    def get_form(self):
        form = super().get_form()
        form.fields['service_date'].widget.attrs.update({'class': 'datepicker'})
        # Sunday service category is single and unique.
        form.fields['categories'].queryset = Category.objects.filter(name__in=SERMON_CATEGORY)
        # Sunday service servants are specific to users of this service category.
        form.fields['servants'].queryset = User.objects.filter(group__name__in=SERMON_GROUP)
        return form

    def form_valid(self, form):
        record = form.cleaned_data
        service_date, service_cat_name = record.get('service_date'), record.get('categories').first().name
        count = Service.objects.filter(service_date=service_date, categories__name__in=[service_cat_name]).count()

        if count > 0:
            messages.warning(self.request, 'Sunday service: %s on %s already existed!' % (service_cat_name, service_date))
        else:
            form.save()
            messages.success(self.request, 'Sunday service: %s on %s was created.' % (service_cat_name, service_date))
        return HttpResponseRedirect(reverse_lazy('sunday_service_list'))


@class_login_required
class SundayServiceListView(django_tables2.SingleTableMixin, FilterView):
    model = Service
    table_class = ServiceTable
    filterset_class = ServiceFilter

    # queryset = Service.objects.filter(categories__name__in=SERMON_CATEGORY)

    template_name = "catalog/sunday_service_list.html"

    table_pagination = {"per_page": 10}

    def get_queryset(self):
        qs = Service.objects.filter(categories__name__in=SERMON_CATEGORY)
        return qs

    def get_table_kwargs(self):
        return {"template_name": "django_tables2/bootstrap.html"}


@class_login_required
class SundayServiceUpdateView(UserPassesTestMixinCustom, SuccessMessageMixin, UpdateView):
    model = Service
    form_class = ServiceForm
    template_name = 'catalog/service_form.html'
    success_url = reverse_lazy('sunday_service_list')
    success_message = 'Sunday Service was updated.'

    def get_form(self):
        form = super(SundayServiceUpdateView, self).get_form()
        form.fields['service_date'].widget.attrs.update({'class': 'datepicker'})
        # Sunday service category is single and unique.
        form.fields['categories'].queryset = Category.objects.filter(name__in=SERMON_CATEGORY)
        # Sunday service servants are specific to users of this service category.
        form.fields['servants'].queryset = User.objects.filter(group__name__in=SERMON_GROUP)
        return form


@class_login_required
class SundayServiceDeleteView(UserPassesTestMixinCustom, DeleteView):
    model = Service
    success_url = reverse_lazy('sunday_service_list')


# Search view
@class_login_required
class SearchListView(ListView):
    template_name = 'catalog/search_results.html'
    paginate_by = 20
    count = 0

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['query'] = self.request.GET.get('q')
        return context

    def get_queryset(self):
        request = self.request
        query = request.GET.get('q', None)

        if query:
            service_results = Service.objects.search(query)
            group_search_results = Group.objects.search(query)
            category_search_results = Category.objects.search(query)
            user_search_results = User.objects.search(query)

            # combine querysets
            queryset_chain = chain(
                service_results,
                group_search_results,
                category_search_results,
                user_search_results
            )
            qs = sorted(queryset_chain,
                        key=lambda instance: instance.pk,
                        reverse=False) # Ascending in pk
            self.count = len(qs)

            return qs
        return Service.objects.none()


# Load services. No permission required.
def load_services(request):
    services = set([s.service_category for s in Service.objects.all()])
    return render(request,
                  'catalog/service_category_list_options.html',
                  {'services': services})


###########
#
#  Export
#
###########

# Export services
@login_required()
@is_staff_or_supervisor
def service_export(request):
    if request.method == 'POST':
        # Get selected option from form
        file_format = request.POST['file-format']
        resource = ServiceResource()
        dataset = resource.export()
        resp = export_data(file_format, dataset,
                           filename=f'service_data-{date2str(dt.now())}')
        return resp
    return render(request, 'helpers/export.html', {'export_url': reverse_lazy('service_export'),
                                                   'data_category': 'Services'})


# Export Sunday sermons
@login_required()
@is_staff_or_supervisor
def sunday_service_export(request):
    if request.method == 'POST':
        # Get selected option from form
        file_format = request.POST['file-format']
        resource = SundaySermonResource()
        dataset = resource.export()
        resp = export_data(file_format, dataset,
                           filename=f'Sunday_sermons_data-{date2str(dt.now())}')
        return resp
    return render(request, 'helpers/export.html', {'export_url': reverse_lazy('sunday_service_export'),
                                                   'data_category': 'Sunday Sermons'})


# Export group
@login_required()
@is_staff_or_supervisor
def export_group_data(request):
    if request.method == 'POST':
        # Get selected option from form
        file_format = request.POST['file-format']
        resource = GroupResource()
        dataset = resource.export()
        resp = export_data(file_format, dataset,
                           filename=f'group_data-{date2str(dt.now())}')
        return resp
    return render(request, 'helpers/export.html', {'export_url': reverse_lazy('group_export'),
                                                   'data_category': 'Groups'})


# Export category
@login_required()
@is_staff_or_supervisor
def export_category_data(request):
    if request.method == 'POST':
        # Get selected option from form
        file_format = request.POST['file-format']
        resource = CategoryResource()
        dataset = resource.export()
        # Invoke export_data function
        resp = export_data(file_format, dataset,
                           filename=f'category_data-{date2str(dt.now())}')
        return resp
    return render(request, 'helpers/export.html', {'export_url': reverse_lazy('category_export'),
                                                   'data_category': 'Categories'})


############
#
# Import
#
############

# # Import services from excel
# @login_required()
# @is_supervisor
# def service_import(request):
#
#     if request.method == 'POST':
#         resource = ServiceResource()
#         dataset = Dataset()
#         loaded_file = request.FILES['external-file']
#
#         imported_data = dataset.load(loaded_file.read())
#         # todo: reopen this function later once figuring out how to install pandas
#         # handle_uploaded_schedules(imported_data, resource)
#
#         # imported_data.headers = ['service_date', 'leader_of_week', 'setup_group', 'food_pickup', 'fruit_dessert',\
#         #                          'dish_clean', 'child_care', 'newcomer_welcome', 'birthday_celebrate', 'worship', 'bible_study',
#         #                          'first visit', 'birthday', 'lunar birthday', 'Habits']
#
#         # convert_first_visit = lambda drow: dt.datetime(1899,12,30)+dt.timedelta(days=int(drow[11])) if drow[11] else None
#
#     return render(request, 'catalog/simple_upload.html')




