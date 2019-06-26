from .views import index, MemberListView, GroupListView, ServiceListView
from .views import MemberDetailView, ServiceDetailView, GroupDetailView
from .views import MemberCreateView, ServiceCreateView
from .views import MemberDeleteView, ServiceDeleteView
from .views import MemberUpdateView, ServiceUpdateView
from .views import CreateAccount
from django.views.generic import (
    RedirectView, TemplateView)
from django.urls import path


urlpatterns = [
    path('', index, name='member_index'),
    path('members/', MemberListView.as_view(), name='member_list'),
    path('member/create/', MemberCreateView.as_view(), name='member_create'),
    path('member/<slug>/detail', MemberDetailView.as_view(), name='member_detail'),
    path('member/<slug>/delete', MemberDeleteView.as_view(), name='member_delete'),
    path('member/<slug>/update', MemberUpdateView.as_view(), name='member_update'),

    path('groups/', GroupListView.as_view(), name='group_list'),
    path('group/<slug>', GroupDetailView.as_view(), name='group_detail'),

    path('services', ServiceListView.as_view(), name='service_list'),
    path('service/create/', MemberCreateView.as_view(), name='service_create'),
    path('service/<slug>/detail', ServiceDetailView.as_view(), name='service_detail'),
    path('service/<slug>/delete', ServiceDeleteView.as_view(), name='service_delete'),
    path('service/<slug>/update', ServiceUpdateView.as_view(), name='service_update'),

]

user_urlpatterns = [
    # create user
    path('create/', CreateAccount.as_view(), name='create'),
    path('create/done/',
         TemplateView.as_view(template_name='user/user_create_done.html'),
         name='create_done'),
]