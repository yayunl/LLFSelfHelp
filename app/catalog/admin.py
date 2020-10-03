from django.contrib import admin
from import_export.admin import ImportExportModelAdmin

# Register your models here.
from .models import Category, Group, Service, ServicesOfWeek
from .resources import ServiceResourceAdmin, GroupResource, CategoryResource


class ServiceAdmin(ImportExportModelAdmin):
    # prepopulated_fields = {'slug': ('name', 'service_date'), }
    # list_display = ['service_date', 'name']
    resource_class = ServiceResourceAdmin
    # exclude = ('slug', 'id')


class GroupAdmin(ImportExportModelAdmin):
    resource_class = GroupResource
    # exclude = ('id', 'slug')


class CategoryAdmin(ImportExportModelAdmin):
    resource_class = CategoryResource


# register the classes
admin.site.register(Group, GroupAdmin)
admin.site.register(Service, ServiceAdmin)
admin.site.register(Category, CategoryAdmin)