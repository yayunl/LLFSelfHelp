from django.shortcuts import render, get_object_or_404
from django.views.generic import View, ListView, DeleteView, DetailView, CreateView, UpdateView
from django.urls import reverse_lazy
from django.http import HttpResponse, HttpResponseRedirect
from django.db.models import Q
from django.db import transaction
from django_filters.views import FilterView

from django.contrib.auth.decorators import login_required
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
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
from .resources import ServiceResource
from .utils import service_dates, str2date #, handle_uploaded_schedules
from .tasks import send_reminders

from users.models import User
from users.utils import SERMON_GROUP, SERMON_CATEGORY


def test_email(request):
    send_reminders.delay()
    return HttpResponse("Email sent.")


# @login_required()
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
        context['member_birthday_of_month'] = User.objects.filter(birthday__month=dt.now().strftime('%m')).all()
        return context


# Groups
# @class_login_required
class GroupCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
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
class GroupUpdateView(SuccessMessageMixin, UpdateView):
    model = Group
    form_class = GroupForm
    success_url = reverse_lazy('group_list')
    success_message = 'Group: %(name)s was updated.'


@class_login_required
class GroupDetailView(DetailView):
    model = Group


@class_login_required
class GroupDeleteView(SuccessMessageMixin, DeleteView):
    model = Group
    success_url = reverse_lazy('group_list')
    success_message = 'Group %(name)s was deleted.'


# Categories
@class_login_required
class CategoryCreateView(SuccessMessageMixin, CreateView):

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
class CategoryUpdateView(SuccessMessageMixin, UpdateView):
    model = Category
    form_class = CategoryForm
    success_url = reverse_lazy('category_list')
    success_message = 'Category: %(name)s was updated.'


@class_login_required
class CategoryDetailView(DetailView):
    model = Category


@class_login_required
class CategoryDeleteView(SuccessMessageMixin, DeleteView):
    model = Category
    success_url = reverse_lazy('category_list')
    success_message = 'Category %(name)s was deleted.'


# Bulk services
class ServiceBulkCreateView(CreateView):
    model = ServicesOfWeek
    form_class = ServicesOfWeekForm
    template_name = 'catalog/service_bulk_create.html'
    success_url = reverse_lazy('service_list')

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
@require_authenticated_permission('catalog.service_create')
class ServiceCreateView(SuccessMessageMixin, CreateView):
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

    table_pagination = {"per_page": 3}

    # def get_table_kwargs(self):
    #     return {"template_name": "django_tables2/bootstrap.html"}


    # def get_queryset(self):
    #     service_date = str2date(service_dates()[0])
    #     queryset = Service.objects.filter(service_date__lt=service_date, service_date__gt=service_date).all()
    #     return queryset


@require_authenticated_permission('catalog.service_update')
class ServiceUpdateView(SuccessMessageMixin, UpdateView):
    model = Service
    form_class = ServiceForm
    success_url = reverse_lazy('service_list')
    success_message = 'The service was updated.'


@require_authenticated_permission('catalog.service_delete')
class ServiceDeleteView(DeleteView):
    model = Service
    success_url = reverse_lazy('service_list')


# Sunday sermons
@require_authenticated_permission('catalog.sunday_service_create')
class SundayServiceCreateView(SuccessMessageMixin, CreateView):
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


@require_authenticated_permission('catalog.sunday_service_update')
class SundayServiceUpdateView(SuccessMessageMixin, UpdateView):
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


@require_authenticated_permission('catalog.sunday_service_create')
class SundayServiceDeleteView(DeleteView):
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
        #todo: reopen this function later once figuring out how to install pandas
        # handle_uploaded_schedules(imported_data, resource)

        # imported_data.headers = ['service_date', 'leader_of_week', 'setup_group', 'food_pickup', 'fruit_dessert',\
        #                          'dish_clean', 'child_care', 'newcomer_welcome', 'birthday_celebrate', 'worship', 'bible_study',
        #                          'first visit', 'birthday', 'lunar birthday', 'Habits']

        # convert_first_visit = lambda drow: dt.datetime(1899,12,30)+dt.timedelta(days=int(drow[11])) if drow[11] else None

    return render(request, 'catalog/simple_upload.html')

