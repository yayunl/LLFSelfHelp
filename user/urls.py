from .views import index, MemberListView, GroupListView, ServiceListView
from .views import MemberDetailView, ServiceDetailView, GroupDetailView
from .views import MemberCreateView
from django.urls import path


urlpatterns = [
    path('', index, name='member_index'),
    path('member/create', MemberCreateView.as_view(), name='member_create'),
    path('members/', MemberListView.as_view(), name='member_list'),
    path('member/<slug>', MemberDetailView.as_view(), name='member_detail'),
    path('groups/', GroupListView.as_view(), name='group_list'),
    path('group/<slug>', GroupDetailView.as_view(), name='group_detail'),
    path('services', ServiceListView.as_view(), name='service_list'),
    path('service/<slug>', ServiceDetailView.as_view(), name='service_detail'),
]