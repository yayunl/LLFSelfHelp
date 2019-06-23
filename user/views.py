from django.shortcuts import render
from django.views.generic import ListView, DeleteView, DetailView, CreateView, UpdateView
from user.models import Group, Member, Service
from user.forms import MemberForm, ServiceForm
from django.urls import reverse_lazy
import datetime as dt



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
    return render(request, 'user/index.html', context=context)


class MemberCreateView(CreateView):
    model = Member
    form_class = MemberForm
    template_name = 'user/member_form.html'


class MemberUpdateView(UpdateView):
    model = Member
    template_name = 'user/member_form.html'
    form_class = MemberForm


class MemberDeleteView(DeleteView):
    model = Member
    # template_name = 'user/member_delete.html'
    success_url = reverse_lazy('member_list')


class MemberListView(ListView):
    model = Member
    context_object_name = 'member_list'
    queryset = Member.objects.filter()
    template_name = 'user/member_list.html'


class MemberDetailView(DetailView):
    model = Member


class GroupListView(ListView):
    model = Group

    context_object_name = 'group_list'
    queryset = Group.objects.filter()
    template_name = 'user/group_list.html'


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
    template_name = 'user/service_list.html'


class ServiceDetailView(DetailView):
    model = Service

    context_object_name = 'service'
    template_name = 'user/service_detail.html'
    queryset = Service.objects.filter()
