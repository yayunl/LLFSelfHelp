from django.urls import path

from .views import IndexView
from .views import ServiceListView, ServiceDetailView, ServiceCreateView, ServiceDeleteView, ServiceUpdateView
from .views import ServiceBulkCreateView
from .views import SundayServiceCreateView, SundayServiceListView, SundayServiceUpdateView, SundayServiceDeleteView
from .views import GroupCreateView, GroupDetailView, GroupListView, GroupDeleteView, GroupUpdateView
from .views import CategoryCreateView, CategoryListView, CategoryDetailView, CategoryUpdateView, CategoryDeleteView
from .views import service_export, service_import, load_services, test_prep_email, test_service_email, test_birthday_email


urlpatterns = [
    path('', IndexView.as_view(), name='catalog_index'),
    # testing tasks
    path('service_email', test_service_email),
    path('prep_email', test_prep_email),
    path('birthday_email', test_birthday_email),

    # Group paths
    path('group/create/', GroupCreateView.as_view(), name='group_create'),
    path('groups/', GroupListView.as_view(), name='group_list'),
    path('group/<slug>/detail', GroupDetailView.as_view(), name='group_detail'),
    path('group/<slug>/update', GroupUpdateView.as_view(), name='group_update'),
    path('group/<slug>/delete', GroupDeleteView.as_view(), name='group_delete'),

    # Category paths
    path('category/create/', CategoryCreateView.as_view(), name='category_create'),
    path('categories/', CategoryListView.as_view(), name='category_list'),
    path('category/<slug>/detail', CategoryDetailView.as_view(), name='category_detail'),
    path('category/<slug>/update', CategoryUpdateView.as_view(), name='category_update'),
    path('category/<slug>/delete', CategoryDeleteView.as_view(), name='category_delete'),

    # Service paths
    path('services', ServiceListView.as_view(), name='service_list'),
    path('services/export', service_export, name='service_export'),
    path('services/import', service_import, name='service_import'),
    path('service/create/', ServiceCreateView.as_view(), name='service_create'),
    path('servicebulk/create/',ServiceBulkCreateView.as_view(), name='service_bulk_create'),
    path('service/<slug>/detail', ServiceDetailView.as_view(), name='service_detail'),
    path('service/<slug>/update', ServiceUpdateView.as_view(), name='service_update'),
    path('service/<slug>/delete', ServiceDeleteView.as_view(), name='service_delete'),


    # load services
    path('ajax/load-services/', load_services, name='ajax_load_services'),

    # Sunday service path
    path('sunday-services', SundayServiceListView.as_view(), name='sunday_service_list'),
    path('sunday-service/create/', SundayServiceCreateView.as_view(), name='sunday_service_create'),
    path('sunday-service/<slug>/update', SundayServiceUpdateView.as_view(), name='sunday_service_update'),
    path('sunday-service/<slug>/delete', SundayServiceDeleteView.as_view(), name='sunday_service_delete')

]
