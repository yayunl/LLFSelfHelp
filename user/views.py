from django.shortcuts import render
from django.views.generic import ListView, DeleteView, DetailView, CreateView
from user.models import Group, Member, Service
from user.forms import MemberForm
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
    today_date = dt.datetime.strptime(today_str, '%Y-%m-%d')
    services = Service.objects.filter(service_date=today_date)
    context = {
        'num_members': num_members,
        'num_groups': num_groups,
        'services': services,
    }

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'user/index.html', context=context)


class MemberCreateView(CreateView):
    model = Member
    form_class = MemberForm
    template_name = 'user/member_create.html'


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
