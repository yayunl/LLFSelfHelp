from django.shortcuts import render
from django.views.generic import ListView, DeleteView, DetailView
from user.models import Group, Member, Service, ServantTeam


def index(request):
    """View function for home page of site."""

    # Generate counts of some of the main objects
    num_members = Member.objects.all().count()
    # num_groups = Service.

    # Available members (status = 'a')
    # num_instances_available = BookInstance.objects.filter(status__exact='a').count()

    # The 'all()' is implied by default.
    num_groups = Group.objects.count()

    context = {
        'num_members': num_members,
        'num_groups': num_groups,
    }

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'user/index.html', context=context)


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


class ServantTeamListView(ListView):
    model = ServantTeam

    context_object_name = 'servant_team_list'
    queryset = ServantTeam.objects.filter()
    template_name = 'user/servant_team_list.html'


class ServantTeamDetailView(DetailView):
    model = ServantTeam

    context_object_name = 'servant_team'
    template_name = 'user/servant_team_detail.html'
