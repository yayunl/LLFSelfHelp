from django.urls import path

from .views import IndexView
from .views import ServiceListView, ServiceDetailView, ServiceCreateView, ServiceDeleteView, ServiceUpdateView
from .views import GroupCreateView, GroupDetailView, GroupListView
from .views import test_email, service_export, service_import, load_services

urlpatterns = [
    path('', IndexView.as_view(), name='catalog_index'),
    path('email', test_email),
    # Groups
    path('groups/', GroupListView.as_view(), name='group_list'),
    path('group/create/', GroupCreateView.as_view(), name='group_create'),
    path('group/<slug>/detail', GroupDetailView.as_view(), name='group_detail'),
    # Services
    path('services', ServiceListView.as_view(), name='service_list'),
    path('services/export', service_export, name='service_export'),
    path('services/import', service_import, name='service_import'),
    path('service/create/', ServiceCreateView.as_view(), name='service_create'),
    path('service/<pk>/detail', ServiceDetailView.as_view(), name='service_detail'),
    path('service/<pk>/delete', ServiceDeleteView.as_view(), name='service_delete'),
    path('service/<pk>/<servicedate>/update', ServiceUpdateView.as_view(), name='service_update'),
    path('ajax/load-services/', load_services, name='ajax_load_services'),
    # Service notes
]
