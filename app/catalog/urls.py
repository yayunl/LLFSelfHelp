from django.urls import path

from .views import IndexView
from .views import ServiceListView, ServiceDetailView, ServiceCreateView, ServiceDeleteView, ServiceUpdateView
from .views import ServiceBulkCreateView
from .views import SundayServiceCreateView, SundayServiceListView, SundayServiceUpdateView, SundayServiceDeleteView
from .views import GroupCreateView, GroupDetailView, GroupListView, GroupDeleteView, GroupUpdateView
from .views import CategoryCreateView, CategoryListView, CategoryDetailView, CategoryUpdateView, CategoryDeleteView
from .views import (load_services, test_prep_email, test_service_email, test_birthday_email, test_coordinator_report_email,
                    service_export, export_group_data, export_category_data)
from .views import admin_page


urlpatterns = [
    path('', IndexView.as_view(), name='home'),
    # testing tasks
    path('service_email', test_service_email),
    path('prep_email', test_prep_email),
    path('birthday_email', test_birthday_email),
    path('report_email', test_coordinator_report_email),
    # admin route
    path('admin', admin_page, name='admin_page'),

    # Group paths
    path('groups/', GroupListView.as_view(), name='group_list'),
    path('group/create/', GroupCreateView.as_view(), name='group_create'),
    path('group/<slug>/detail', GroupDetailView.as_view(), name='group_detail'),
    path('group/<slug>/update', GroupUpdateView.as_view(), name='group_update'),
    path('group/<slug>/delete', GroupDeleteView.as_view(), name='group_delete'),
    path('group/export', export_group_data, name='group_export'),

    # Category paths
    path('categories/', CategoryListView.as_view(), name='category_list'),
    path('category/create/', CategoryCreateView.as_view(), name='category_create'),
    path('category/<slug>/detail', CategoryDetailView.as_view(), name='category_detail'),
    path('category/<slug>/update', CategoryUpdateView.as_view(), name='category_update'),
    path('category/<slug>/delete', CategoryDeleteView.as_view(), name='category_delete'),
    path('category/export', export_category_data, name='category_export'),

    # Service paths
    path('services', ServiceListView.as_view(), name='service_list'),
    path('service/create/', ServiceCreateView.as_view(), name='service_create'),
    path('servicebulk/create/',ServiceBulkCreateView.as_view(), name='service_bulk_create'),
    path('service/<slug>/detail', ServiceDetailView.as_view(), name='service_detail'),
    path('service/<slug>/update', ServiceUpdateView.as_view(), name='service_update'),
    path('service/<slug>/delete', ServiceDeleteView.as_view(), name='service_delete'),
    path('services/export', service_export, name='service_export'),
    # path('services/import', service_import, name='service_import'),


    # load services
    path('ajax/load-services/', load_services, name='ajax_load_services'),

    # Sunday service path
    path('sunday-services', SundayServiceListView.as_view(), name='sunday_service_list'),
    path('sunday-service/create/', SundayServiceCreateView.as_view(), name='sunday_service_create'),
    path('sunday-service/<slug>/update', SundayServiceUpdateView.as_view(), name='sunday_service_update'),
    path('sunday-service/<slug>/delete', SundayServiceDeleteView.as_view(), name='sunday_service_delete')

]
