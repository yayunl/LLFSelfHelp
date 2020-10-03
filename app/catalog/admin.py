from django.contrib import admin
from import_export.admin import ImportExportModelAdmin

# Register your models here.
from .models import Category, Group, Service, ServicesOfWeek
from .resources import ServiceResourceAdmin, GroupResourceAdmin, CategoryResourceAdmin


class ServiceAdmin(ImportExportModelAdmin):
    resource_class = ServiceResourceAdmin


class GroupAdmin(ImportExportModelAdmin):
    resource_class = GroupResourceAdmin
    # exclude = ('id', 'slug')


class CategoryAdmin(ImportExportModelAdmin):
    resource_class = CategoryResourceAdmin


# register the classes
admin.site.register(Group, GroupAdmin)
admin.site.register(Service, ServiceAdmin)
admin.site.register(Category, CategoryAdmin)