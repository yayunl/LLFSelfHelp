from django.shortcuts import render, get_object_or_404
from django.views.generic import View, ListView, DeleteView, DetailView, CreateView, UpdateView
from django.urls import reverse_lazy
from django.http import HttpResponse
from django.db.models import Q
from django_filters.views import FilterView
import django_tables2
from tablib import Dataset
from django.contrib.auth.decorators import login_required
from .decorators import class_login_required, require_authenticated_permission
from datetime import datetime as dt
from itertools import chain

# sub-level imports
from .models import Group, Service, Category
from users.models import User
from .tables import ServiceTable, ServiceFilter
from .forms import ServiceForm, GroupForm, CategoryForm
from .resources import ServiceResource
from .utils import handle_uploaded_schedules, service_dates, str2date
from users.utils import SERMON_GROUP, SERMON_CATEGORY
from .tasks import send_reminders


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
@class_login_required
class GroupCreateView(CreateView):
    model = Group
    template_name = 'catalog/group_form.html'
    form_class = GroupForm
    success_message = 'Success: Group was created.'
    success_url = reverse_lazy('group_list')


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
class GroupUpdateView(UpdateView):
    model = Group
    form_class = GroupForm
    success_url = reverse_lazy('group_list')


@class_login_required
class GroupDetailView(DetailView):
    model = Group


@class_login_required
class GroupDeleteView(DeleteView):
    model = Group
    success_url = reverse_lazy('group_list')


# Categories
@class_login_required
class CategoryCreateView(CreateView):
    model = Category
    template_name = 'catalog/group_form.html'
    form_class = CategoryForm
    success_message = 'Success: Category was created.'
    success_url = reverse_lazy('category_list')


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
class CategoryUpdateView(UpdateView):
    model = Category
    form_class = CategoryForm
    success_url = reverse_lazy('category_list')


@class_login_required
class CategoryDetailView(DetailView):
    model = Category


@class_login_required
class CategoryDeleteView(DeleteView):
    model = Category
    success_url = reverse_lazy('category_list')


# Services
@require_authenticated_permission('catalog.service_create')
class ServiceCreateView(CreateView):
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

    success_url = reverse_lazy('service_list')


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

    def get_table_kwargs(self):
        return {"template_name": "django_tables2/bootstrap.html"}


@require_authenticated_permission('catalog.service_update')
class ServiceUpdateView(UpdateView):
    model = Service
    form_class = ServiceForm
    success_url = reverse_lazy('service_list')


@require_authenticated_permission('catalog.service_delete')
class ServiceDeleteView(DeleteView):
    model = Service
    success_url = reverse_lazy('service_list')


# Sunday sermons
@require_authenticated_permission('catalog.sunday_service_create')
class SundayServiceCreateView(CreateView):
    model = Service
    form_class = ServiceForm
    template_name = 'catalog/service_form.html'

    queryset = Service.objects.filter()

    def get_form(self):
        form = super(SundayServiceCreateView, self).get_form()
        form.fields['service_date'].widget.attrs.update({'class': 'datepicker'})
        # Sunday service category is single and unique.
        form.fields['categories'].queryset = Category.objects.filter(name__in=SERMON_CATEGORY)
        # Sunday service servants are specific to users of this service category.
        form.fields['servants'].queryset = User.objects.filter(group__name__in=SERMON_GROUP)
        return form

    success_url = reverse_lazy('service_list')


@class_login_required
class SundayServiceListView(django_tables2.SingleTableMixin, FilterView):
    model = Service
    table_class = ServiceTable
    filterset_class = ServiceFilter

    queryset = Service.objects.filter(categories__name__in=SERMON_CATEGORY)

    template_name = "catalog/sunday_service_list.html"

    table_pagination = {"per_page": 10}

    def get_table_kwargs(self):
        return {"template_name": "django_tables2/bootstrap.html"}


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
        handle_uploaded_schedules(imported_data, resource)
        # imported_data.headers = ['service_date', 'leader_of_week', 'setup_group', 'food_pickup', 'fruit_dessert',\
        #                          'dish_clean', 'child_care', 'newcomer_welcome', 'birthday_celebrate', 'worship', 'bible_study',
        #                          'first visit', 'birthday', 'lunar birthday', 'Habits']

        # convert_first_visit = lambda drow: dt.datetime(1899,12,30)+dt.timedelta(days=int(drow[11])) if drow[11] else None

    return render(request, 'catalog/simple_upload.html')

