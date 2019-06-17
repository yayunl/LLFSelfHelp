from .views import index, MemberListView, MemberDetailView, GroupListView, GroupDetailView
from django.urls import path


urlpatterns = [
    path('', index, name='member_index'),
    path('members/', MemberListView.as_view(), name='member_list'),
    path('member/<slug>', MemberDetailView.as_view(), name='member_detail'),
    path('groups/', GroupListView.as_view(), name='group_list'),
    path('group/<slug>', GroupDetailView.as_view(), name='group_detail'),
]