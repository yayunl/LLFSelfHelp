from django.shortcuts import render, get_object_or_404
from django.views.generic import View, ListView, DeleteView, DetailView, CreateView, UpdateView
from django.urls import reverse_lazy
from django.http import HttpResponse
from django_filters.views import FilterView
import django_tables2
from tablib import Dataset
from django.contrib.auth.decorators import login_required
from .decorators import class_login_required, require_authenticated_permission

# sub-level imports
from .models import Group, Service, Category
from .tables import ServiceTable, ServiceFilter
from .forms import ServiceForm, GroupForm, CategoryForm
from .resources import ServiceResource
from .utils import handle_uploaded_schedules, service_dates, str2date
from .tasks import send_reminders


def test_email(request):
    send_reminders.delay()
    return HttpResponse("Email sent.")


# @login_required()
class IndexView(ListView):
    model = Service
    # table_class = ServiceTable

    # Query services of this week
    queryset = Service.objects.filter(service_date=str2date(service_dates()[0]))
    context_object_name = 'services'
    template_name = "catalog/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        this_week_service_date_str, following_service_date_str, _ = service_dates()
        # services = Service.objects.filter(service_date=this_week_service_date_str)
        following_week_services = Service.objects.filter(service_date=str2date(following_service_date_str))

        context['next_week_services'] = following_week_services

        context['this_week_service_date'] = this_week_service_date_str
        context['next_week_service_date'] = following_service_date_str
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
    queryset = Group.objects.filter()
    template_name = 'catalog/group_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['create_url'] = reverse_lazy('group_create')
        return context


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
    queryset = Category.objects.filter()
    template_name = 'catalog/category_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['create_url'] = reverse_lazy('category_create')
        return context


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


# @class_login_required
# class ServiceListView(ListView):
#     model = Service
#     context_object_name = 'service_list'
#     queryset = Service.objects.filter()
#     template_name = 'catalog/service_list.html'



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

